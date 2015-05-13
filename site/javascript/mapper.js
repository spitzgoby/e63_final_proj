d3.selection.prototype.moveToFront = function() {
  return this.each(function(){
  this.parentNode.appendChild(this);
  });
};

var mapper = {
  geoDirectory:  "../data/geo/",

  drawUSA : function() {
    mapper.drawCountryMap("us", this.geoDirectory + "us_borders.json", 350, [-117, 47]);
  },

  drawChina : function() {
    mapper.drawCountryMap("china", this.geoDirectory + "china_borders.json", 700, [105, 37.5]);
  },

  drawWorld : function() {
    mapper.drawCountryMap("world", this.geoDirectory + "world_borders.json", 110, [0,0])
  },
  
  drawCountryMap : function(name, jsonFile, scale, center) {
    var mapWidth = 800, mapHeight = 700,
        listWidth = 400, listHeight = 700;

    var map = d3.select("svg.map");
    if (map.size() == 0) {
      map = d3.select("div#map-container").append("svg")
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
      // draw country borders
      map.append("path")
        .datum(topojson.feature(country, country.objects[name]))
        .attr("d", path)
        .attr("class", "country-border");

      // remove old city circles 
      map.select("circle.city").remove();
      var fileName = "../data/interactions/top_cities_" + name + ".csv";
      d3.text(fileName, function(text){
        var data = d3.csv.parseRows(text, function(row, i) {
          if (i < 10) {
            return {
              "name": row[0],
              "latitude": +row[2],
              "longitude": +row[3],
              "count": +row[4]
            };
          } else {
            return null;
          }
        });

        var map = d3.select("svg.map");
        map.selectAll(".city").data(data).enter().append("circle")
          .attr("class", "city")
          .attr("cx", function(d) {
            return projection([d.longitude, d.latitude])[0];})
          .attr("cy", function(d) {
            return projection([d.longitude, d.latitude])[1];})
          .attr("r", 10)
          .attr("id", function(d) { return d.name.replace(/[\s\.]/g,'')});

        var list = d3.select("ol#cities-list");
        list.selectAll("p").remove();
        list.selectAll("p").data(data).enter().append("li")
          .text(function(d) { return d.name })
          .on("mouseover", function(d) {
            d3.select(this)
              .attr("class", "active");
            d3.select("#" + d.name.replace(/[\s\.]/g,''))
              .moveToFront()
              .transition()
              .attr("r", 100);

            var coords = projection([d.longitude, d.latitude]);
            map.append("text")
              .attr("text-anchor", "middle")
              .attr("x", coords[0])
              .attr("y", coords[1])
              .attr("id", d.name.replace(/[\s\.]/g,'') + "count-label")
              .text(d.name + " " + d.count);
          })
          .on("mouseout", function(d) {
            d3.select(this)
              .attr("class", null);
            d3.select("#" + d.name.replace(/[\s\.]/g,''))
              .transition()
              .attr("r", 10);
            d3.select("#" + d.name.replace(/[\s\.]/g,'') + "count-label").remove();
          }); 
      });
    }); 
  }
}