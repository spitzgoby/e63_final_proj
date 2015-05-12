package e63.thomasleu.final_asn

import java.util.UUID

import org.apache.spark.{SparkContext, SparkConf}
import com.datastax.spark.connector._

/**
 * Created by Thomas Leu
 */
object InteractionCities {
  case class Interaction(user_id: UUID, time_stamp: Double, duration: Double, latitude: Double, longitude: Double)
  case class InteractionCity(user_id: UUID, time_stamp: Double, duration: Double, city: City)

  def main(args: Array[String]): Unit = {
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

    // grab interaction data from Cassandra and map cities to them. For this job there is no
    // reduce phase.
    val interactions = sc.cassandraTable[Interaction]("e63", "interactions")
    val interactionCities = interactions.map(x => {
        InteractionCity(x.user_id, x.time_stamp, x.duration, nearestCity(x, cityTree))
    })

    // save the results
    interactionCities.saveAsTextFile("InteractionCities")
  }

  /** *
    * Finds the city nearest to the given interaction
    * @param interaction The user interaction for which to find a city
    * @param cities A k-d tree of the possible city choices
    * @return The closest city. If multiple cities are equidistant from the given interaction no guarantee is made
    *         about which city is returned. Returns null if no interaction or city is passed
    * @see CityKDTreeFactory.scala for information about creating CityKDTrees
    */
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
