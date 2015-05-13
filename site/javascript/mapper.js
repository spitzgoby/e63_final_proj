var mapper = {
  dataDirectory: "../data/geo/",

  drawUSA : function() {
    mapper.drawCountryMap("us", this.dataDirectory + "us_borders.json", 660, [-96, 38]);
  },

  drawChina : function() {
    mapper.drawCountryMap("china", this.dataDirectory + "china_borders.json", 640, [104.5, 37.5]);
  },

  drawWorld : function() {
    mapper.drawCountryMap("world", this.dataDirectory + "world_borders.json", 110, [0,0])
  },
  
  drawCountryMap : function(name, jsonFile, scale, center) {
    var mapWidth = 700,
        mapHeight = 700;

    var map = d3.select("svg.map");
    if (map.size() == 0) {
      map = d3.select("div#data").append("svg")
        .attr("width", mapWidth)
        .attr("height", mapHeight)
        .attr("class", "map");
    }

    var projection = d3.geo.mercator()
      .scale(scale)
      .center(center)
      .translate([mapWidth / 2, mapHeight / 2]);
    var path = d3.geo.path()
      .projection(projection);

    d3.json(jsonFile, function(error, country) {
      if (error) return console.error(error);

    map.append("path")
      .datum(topojson.feature(country, country.objects[name]))
      .attr("d", path)
      .attr("class", "country-border");
    }); 
  }
}