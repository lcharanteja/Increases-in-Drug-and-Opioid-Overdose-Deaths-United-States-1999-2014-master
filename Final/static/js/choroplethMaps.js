d3.select("#map").html("")
var globalYear = 1999
$('#sliderYear').on('input change', function () {
        $('#rangeText').text($(this).val());
    });

d3.selectAll('input[name="sliderYear"]').on("change",function(){globalYear=this.value;
                                              $.getJSON($SCRIPT_ROOT + '/filterDataByYear', {
                                                year: this.value
                                              }, function(data) {
                                                var filterType = d3.select('input[name="filter"]:checked').node().value
                                                
                                                var map = d3.geomap.choropleth()
                                                            .geofile('./static/d3-geomap/topojson/countries/USA.json')
                                                            .colors(colorbrewer.YlGnBu[9])
                                                            .projection(d3.geo.albersUsa)
                                                            .column(filterType)
                                                            .unitId('Id')
                                                            .scale(600)
                                                            .legend(true);

                                                d3.csv('./static/data/temp-map-data/temp'+globalYear+'.csv', function(error, data) {
                                    
                                                    d3.select('#map').html("")
                                                        .datum(data)
                                                        .call(map.draw, map);
                                                });
                                              });
                                              return false;
                                    });
d3.select('#slider').call(d3.slider().axis(true).min(1999).max(2014).step(1)
                            .on("slide", function(evt, value) {
                                $(function() {globalYear=value
                                              $.getJSON($SCRIPT_ROOT + '/filterDataByYear', {
                                                year: value
                                              }, function(data) {
                                                console.log(data);
                                                var filterType = d3.select('input[name="filter"]:checked').node().value
                                                
                                                var map = d3.geomap.choropleth()
                                                            .geofile('./static/d3-geomap/topojson/countries/USA.json')
                                                            .colors(colorbrewer.YlGnBu[9])
                                                            .projection(d3.geo.albersUsa)
                                                            .column(filterType)
                                                            .unitId('Id')
                                                            .scale(600)
                                                            .legend(true);

                                                d3.csv('./static/data/temp-map-data/temp'+value+'.csv', function(error, data) {
                                    
                                                    d3.select('#map').html("")
                                                        .datum(data)
                                                        .call(map.draw, map);
                                                });
                                              });
                                              return false;
                                          });

                            }));

d3.selectAll('input[name="filter"]').on("change", function(){

    var map = d3.geomap.choropleth()
    .geofile('./static/d3-geomap/topojson/countries/USA.json')
    .colors(colorbrewer.YlGnBu[9])
    .projection(d3.geo.albersUsa)
    .column(this.value)
    .unitId('Id')
    .scale(600)
    .legend(true);
        
d3.csv('./static/data/temp-map-data/temp'+globalYear+'.csv', function(error, data) {
    d3.select('#map')
    .html("")
        .datum(data)
        .call(map.draw, map);
});

});


var map = d3.geomap.choropleth()
    .geofile('./static/d3-geomap/topojson/countries/USA.json')
    .colors(colorbrewer.YlGnBu[9])
    .projection(d3.geo.albersUsa)
    .column('Deaths')
    .unitId('Id')
    .scale(600)
    .legend(true)
        

d3.csv('./static/data/temp-map-data/temp1999.csv', function(error, data) {
    d3.select('#map')
    .html("")
        .datum(data)
        .call(map.draw, map);
});

