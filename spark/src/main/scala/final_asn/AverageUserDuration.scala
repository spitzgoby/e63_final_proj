package final_asn

import java.util.UUID

import org.apache.spark.SparkContext
import org.apache.spark.SparkConf
import org.apache.spark.SparkContext._
import com.datastax.spark.connector._

/**
 * Created by Thomas Leu
 *
 * Some code adapted from code originally found in "Learning Spark" by
 * Matei Zaharia; Patrick Wendell; Holden Karau; Andy Konwinski, O'Reilly Books Copyright 2015
 * https://www.safaribooksonline.com/library/view/learning-spark/9781449359034/ch04.html#chap-pair-RDDS
 *
 */
object AverageUserDuration {

  private final val E63_KEYSPACE = "e63"
  private final val INTERACTIONS_TABLE = "interactions"

  case class Interaction(user_id: UUID, time_stamp: Double, duration: Double, latitude: Double, longitude: Double)

  def main(args: Array[String]) {
    // prepare Spark to use local Cassandra DB
    val conf = new SparkConf()
      .setMaster("local")
      .setAppName("AverageUserDuration")
      .set("spark.cassandra.connection.host", "127.0.0.1")
    val sc = new SparkContext(conf)

    // grab all interactions and calculate the average.
    // Code adapted from source code originally found in "Learning Spark" by
    // Matei Zaharia; Patrick Wendell; Holden Karau; Andy Konwinski, O'Reilly Books Copyright 2015
    // https://www.safaribooksonline.com/library/view/learning-spark/9781449359034/ch04.html#chap-pair-RDDS
    val interactions = sc.cassandraTable[Interaction](this.E63_KEYSPACE, this.INTERACTIONS_TABLE)
    val averages = interactions.map(interaction => (interaction.user_id, interaction.duration)).combineByKey(
      (duration: Double) => (duration, 1),
      (acc: (Double, Int), duration: Double) => (acc._1 + duration, acc._2 + 1),
      (acc1: (Double, Int), acc2: (Double, Int)) => (acc1._1 + acc2._1, acc1._2 + acc2._2)
    ).map{case (user_id, (total_dur, num_interactions)) => (user_id, total_dur / num_interactions)}
    averages.saveAsTextFile("user_averages")
  }
}
