# Instructiosn modified from examples provided at 
# http://bost.ocks.org/mike/map/

# create china.json
ogr2ogr -f GeoJSON -where "adm0_a3 IN ('CHN', 'HKG', 'TWN')" \
  china.json ne_110m_admin_0_map_units.shp;

# create us.json
ogr2ogr -f GeoJSON -where "adm0_a3 IN ('USA')" \
  us.json ne_110m_admin_0_map_units.shp;

# create world.json
ogr2ogr -f GeoJSON world.json ne_110m_admin_0_map_units.shp;

# create topojson border objects for d3 to read
topojson -o us_borders.json --id-property SU_A3 -- us.json;
topojson -o china_borders.json --id-property SU_A3 -- china.json;
topojson -o world_borders.json --id_proprety SU_A3 -- world.json;

# move files to data directory
mkdir data;
mkdir data/geo;
mv *.json data/geo;