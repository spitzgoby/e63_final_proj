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
    val conf = new SparkConf()
      .setMaster("local")
      .setAppName("InteractionCities")
      .set("spark.cassandra.connection.host", "127.0.0.1")
    val sc = new SparkContext(conf)

    val citiesRDD = sc.cassandraTable[City]("e63", "cities")
    val cities = citiesRDD.collect().toList
    val cityTree = new CityKDTreeFactory().kdTree(cities)

    val interactions = sc.cassandraTable[Interaction]("e63", "interactions")
    val interactionCities = interactions.map(x => {
        InteractionCity(x.user_id, x.time_stamp, x.duration, nearestCity(x, cityTree))
    })

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
    if (cities.isleaf) {
      cities.root
    } else {
      if (cities.root.name == "Beijing" || cities.root.name == "Qinhuangdao") {
        val pause = 0
      }

      var nextChild , otherChild : CityKDTree = null
      if (traverseLeft(interaction, cities.root, depth)) {
        nextChild = cities.leftChild
        otherChild = cities.rightChild
      } else {
        nextChild = cities.rightChild
        otherChild = cities.leftChild
      }

      // prepare variables and values
      var minimumDistance = Double.MaxValue
      var closest : City = null

      // recursively check next child (if exists)
      if (nextChild != null) {
        closest = nearestCity(interaction, nextChild, depth + 1)
        minimumDistance = locationDistance(interaction, closest)
      }


      // if distance to hyperplane is less than distance from current closest city check other child
      if (minimumDistance >= planeDistance(interaction, cities.root, depth) && otherChild != null) {
        val otherClosest = nearestCity(interaction, otherChild, depth + 1)
        val otherDistance = locationDistance(interaction, otherClosest)
        if (otherDistance < minimumDistance) {
          closest = otherClosest
        }
      }

      // check the current city against the current best
      val nodeDistance = locationDistance(interaction, cities.root)
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


  def planeDistance(interaction: Interaction, city: City, depth : Int) : Double = {
    if (depth % 2 == 0) {
      Math.pow(interaction.latitude - city.latitude, 2)
    } else {
      Math.pow(interaction.longitude - city.longitude, 2)
    }
  }

  def locationDistance(interaction: Interaction, city: City) : Double = {
    math.pow(interaction.latitude - city.latitude, 2) + math.pow(interaction.longitude - city.longitude, 2)
  }
}
