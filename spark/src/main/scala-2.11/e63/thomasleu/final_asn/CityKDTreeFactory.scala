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

