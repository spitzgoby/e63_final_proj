package e63.thomasleu.final_asn

/**
 * Created by Thomas Leu
 */

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

  def kdTree(cities: List[City]) : CityKDTree = {
    kdTree(cities, 0)
  }

  private def kdTree(cities: List[City], depth: Int) : CityKDTree = {
    cities.length match {
      case 0 => null
      case 1 =>
        new CityKDTree(
          root = cities.head,
          leftChild = null,
          rightChild = null
        )
      case _ =>
        val sortedCities = cities.sortWith((x, y) => {
          if (depth % 2 == 0) x.latitude < y.latitude
          else x.longitude < y.longitude})

        val median = cities.length / 2

        if (cities(median).name == "Qinhuangdao") {
          val pause = 0
        }
        new CityKDTree(
          root = sortedCities(median),
          leftChild = kdTree(sortedCities.slice(0,median), depth + 1),
          rightChild = kdTree(sortedCities.slice(median+1, cities.length), depth + 1))
    }
  }
}

