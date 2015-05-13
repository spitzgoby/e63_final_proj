package final_asn

import java.util.UUID
import org.apache.spark.{SparkContext, SparkConf}
import org.apache.spark.SparkContext._
import com.datastax.spark.connector._

/**
 * Created by Thomas Leu
 */
case class Interaction(user_id: UUID, time_stamp: Double, duration: Double, latitude: Double, longitude: Double)
case class City (name: String, latitude: Double, longitude: Double, country: String)
case class CityKDTree(root: City, leftChild: CityKDTree, rightChild: CityKDTree) {
  def isleaf : Boolean = (leftChild == null) && (rightChild == null)
  def count : Int = {
    (leftChild, rightChild) match {
      case (null, null) => 1
      case (l, null) => l.count + 1
      case (null, r) => r.count + 1
      case (l, r) => l.count + r.count + 1
    }
  }
}

class CityKDTreeFactory {
  /** *
    * Creates a CityKDTree from a list of City objects
    * @param cities The list of cities to make into a CityKDTree
    * @return A CityKDTree with the cities split by latitude on even-leveled nodes and longitude
    *         on odd-leveled nodes
    * @see http://en.wikipedia.org/wiki/K-d_tree
    */
  def kdTree(cities: List[City]) : CityKDTree = {
    kdTree(cities, 0)
  }

  private def kdTree(cities: List[City], depth: Int) : CityKDTree = {
    cities.length match {
      case 0 => null // no more cities
      case 1 => // leaf node
        new CityKDTree(
          root = cities.head,
          leftChild = null,
          rightChild = null
        )
      case _ => // branch node
        // sort cities by latitude on even branches and longitude on odd branches
        val sortedCities = cities.sortWith((x, y) => {
          if (depth % 2 == 0) x.latitude < y.latitude
          else x.longitude < y.longitude})

        val median = cities.length / 2

        new CityKDTree( // set root to median value and split left and right side into planes
          root = sortedCities(median),
          leftChild = kdTree(sortedCities.slice(0,median), depth + 1),
          rightChild = kdTree(sortedCities.slice(median+1, cities.length), depth + 1))
    }
  }
}


object TopInteractionCities {
  def main(args: Array[String]) {
    var targetCountry = "world"
    if (args.length >= 1) {
      targetCountry = args(0)
    }

    // prepare Spark to use local Cassandra DB
    val conf = new SparkConf()
      .setMaster("local")
      .setAppName("InteractionCities")
      .set("spark.cassandra.connection.host", "127.0.0.1")
    val sc = new SparkContext(conf)

    // grab city data from Cassandra and build a k-d tree
    val citiesRDD = sc.cassandraTable[City]("e63", "cities")
    val cities = citiesRDD.collect().toList
    val cityTree = new CityKDTreeFactory().kdTree(cities)

    // grab interaction data from Cassandra and map cities to them to (City, duration) pairs
    val interactions = sc.cassandraTable[Interaction]("e63", "interactions")
    val countryInteractions = interactions.map(x => {
      (nearestCity(x, cityTree), x.duration)
    }).combineByKey(
        (duration: Double) => (duration, 1),
        (acc: (Double, Int), duration: Double) => (acc._1 + duration, acc._2 + 1),
        (acc1: (Double, Int), acc2: (Double, Int)) => (acc1._1 + acc2._1, acc1._2 + acc2._2)
      ).filter{ case (city, (_, _)) => if (targetCountry.equalsIgnoreCase("world")) true else {city.country.equalsIgnoreCase(targetCountry)}}
      .map{case (city, (total_dur, num_interactions)) => (city.name, city.country, city.latitude, city.longitude, num_interactions)}
    // print all cities with interactions into a comma separated value file sorted by country
    countryInteractions.sortBy{ case (_, _, _, _, num_interactions) => -num_interactions}
      .map{ case (name, country, latitude, longitude, num_interactions) => Array(name, country, latitude, longitude, num_interactions).mkString(",")}
      .saveAsTextFile("top_cities_" + targetCountry)
  }

  def nearestCity(interaction: Interaction, cities: CityKDTree) : City = {
    if (interaction == null || cities == null) return null
    nearestCity(interaction, cities, 0)
  }

  private def nearestCity(interaction: Interaction, cities: CityKDTree, depth: Int) : City = {
    // base case, leaf node is current best
    if (cities.isleaf) {
      cities.root
    } else {

      // declare and initialize variables so they can be accessed within if statements
      var nextChild , otherChild : CityKDTree = null
      var minimumDistance = Double.MaxValue
      var closest : City = null

      // determine which direction to search initially
      if (traverseLeft(interaction, cities.root, depth)) {
        nextChild = cities.leftChild
        otherChild = cities.rightChild
      } else {
        nextChild = cities.rightChild
        otherChild = cities.leftChild
      }

      // recursively check next child (if it exists) and set minimum value to this city's value
      if (nextChild != null) {
        closest = nearestCity(interaction, nextChild, depth + 1)
        minimumDistance = locationDistanceSquared(interaction, closest)
      }

      // if distance to hyperplane is less than distance from current closest city check other child
      if (minimumDistance >= planeDistanceSquared(interaction, cities.root, depth) && otherChild != null) {
        // the distance to the split plane is less than the current minimum distance so the closest city could
        // be in the other tree
        val otherClosest = nearestCity(interaction, otherChild, depth + 1)
        val otherDistance = locationDistanceSquared(interaction, otherClosest)
        if (otherDistance < minimumDistance) {
          closest = otherClosest
        }
      }

      // finally, check the current city against the current best
      val nodeDistance = locationDistanceSquared(interaction, cities.root)
      if (nodeDistance < minimumDistance) {
        closest = cities.root
      } else if (nodeDistance == minimumDistance) {
        closest = cities.root
      }

      closest
    }
  }

  private def traverseLeft(interaction: Interaction, city: City, depth: Int) : Boolean = {

    if (depth % 2 == 0) { // use latitude
      interaction.latitude < city.latitude
    } else { // use longitude
      interaction.longitude < city.longitude
    }
  }


  private def planeDistanceSquared(interaction: Interaction, city: City, depth : Int) : Double = {
    // the square is returned for efficiency reasons
    if (depth % 2 == 0) { // use latitude
      Math.pow(interaction.latitude - city.latitude, 2)
    } else { // use longitude
      Math.pow(interaction.longitude - city.longitude, 2)
    }
  }

  /** *
    * Calculates the square of the distance between an interaction and a city.
    * @param interaction The user interaction with which to find distance
    * @param city The city from which to find distance
    * @return The square of the distance between the city and the interaction
    */
  def locationDistanceSquared(interaction: Interaction, city: City) : Double = {
    // the square is returned for efficiency reasons
    math.pow(interaction.latitude - city.latitude, 2) + math.pow(interaction.longitude - city.longitude, 2)
  }
}
