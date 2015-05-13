package e63.thomasleu.final_asn

import e63.thomasleu.final_asn.InteractionCities.Interaction
import org.apache.spark.{SparkContext, SparkConf}
import org.apache.spark.SparkContext._
import com.datastax.spark.connector._

/**
 * Created by Thomas Leu
 */
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
      (InteractionCities.nearestCity(x, cityTree), x.duration)
    }).combineByKey(
        (duration: Double) => (duration, 1),
        (acc: (Double, Int), duration: Double) => (acc._1 + duration, acc._2 + 1),
        (acc1: (Double, Int), acc2: (Double, Int)) => (acc1._1 + acc2._1, acc1._2 + acc2._2)
      ).filter{ case (city, (_, _)) => if (targetCountry.equalsIgnoreCase("world")) true else {city.country.equalsIgnoreCase(targetCountry)}}
      .map{case (city, (total_dur, num_interactions)) => (city.name, city.country, city.latitude, city.longitude, num_interactions)}
    // print all cities with interactions into a comma separated value file sorted by country
    countryInteractions.sortBy{ case (_, _, _, _, num_interactions) => -num_interactions}
      .map{ case (name, country, latitude, longitude, num_interacitons) => Array(name, country, latitude, longitude, num_interacitons).mkString(",")}
      .saveAsTextFile("top_cities_" + targetCountry)
  }
}
