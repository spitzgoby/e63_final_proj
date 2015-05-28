package final_asn

import InteractionCities.Interaction
import org.apache.spark.SparkContext
import org.apache.spark.SparkConf
import org.apache.spark.SparkContext._
import com.datastax.spark.connector._

/**
 * Created by Thomas Leu
 */
object AverageUserDurationPerCity {
  def main(args: Array[String]) {
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
    val avgCityDurations = interactions.map(x => {
      (InteractionCities.nearestCity(x, cityTree), x.duration)
    }).combineByKey(
        (duration: Double) => (duration, 1),
        (acc: (Double, Int), duration: Double) => (acc._1 + duration, acc._2 + 1),
        (acc1: (Double, Int), acc2: (Double, Int)) => (acc1._1 + acc2._1, acc1._2 + acc2._2)
      ).filter{ case (_, (_, num_interactions)) => num_interactions > 2}
      .map{case (city, (total_dur, num_interactions)) => (city.name, city.country, total_dur / num_interactions)}
    // print all cities with interactions into a comma separated value file sorted by country
    avgCityDurations.sortBy{ case (_, country, _) => country}
      .map{ case (name, country, avgDuration) => Array(name, country, avgDuration).mkString(",")}
      .saveAsTextFile("average_city_duration")
  }

}
