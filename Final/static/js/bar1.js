 $.getJSON($SCRIPT_ROOT + '/getGenderData', {race : $('input[name="filter"]:checked').val(),year:$('input[name="sliderYear"]').val()}, function(d) { horbar1(d,"#barGender");});
 $.getJSON($SCRIPT_ROOT + '/getAgeGroupData', {race : $('input[name="filter"]:checked').val(),year:$('input[name="sliderYear"]').val()}, function(d) { horbar1(d,"#barAge");});
 d3.selectAll('input[name="filter"]').on("change", change);
  $('#sliderYear').on('input change', function () {
        $('#rangeText').text($(this).val());
    });
  d3.selectAll('input[name="sliderYear"]').on("change", change);


function horbar1(data, div){
    d3.select(div).html("");
    var raceFilter = d3.select('input[name="filter"]:checked').node().value
    var yearFilter = d3.select('input[name="sliderYear"]').node().value
    d3.selectAll(".ageracespan").html(raceFilter);
    d3.selectAll(".ageyearspan").html(yearFilter);


    var svg = d3.select(div).append("svg")
            .attr("width", 400)
            .attr("height", 300),
    margin = {top: 20, right: 20, bottom: 30, left: 80},
    width = +svg.attr("width") - margin.left - margin.right,
    height = +svg.attr("height") - margin.top - margin.bottom;

    var color = d3.scaleOrdinal(d3.schemeCategory20b);
  
var tooltip = d3.select("body").append("div").attr("class", "toolTip");
  
var x = d3.scaleLinear().range([0, width]);
var y = d3.scaleBand().range([height, 0]);



var g = svg.append("g")
        .attr("transform", "translate(" + margin.left + "," + margin.top + ")");
  
  
   /* data.sort(function(a, b) { return b.value - a.value; });*/
  
    x.domain([0, d3.max(data, function(d) { return d.value; })]);
    y.domain(data.map(function(d) { return d.label; })).padding(0.1);

    g.append("g")
        .attr("class", "x axis")
        .attr("transform", "translate(0," + height + ")")
        .call(d3.axisBottom(x).ticks(8).tickFormat(d3.formatPrefix(".1", 1e4)).tickSizeInner([-height]));

    g.append("g")
        .attr("class", "y axis")
        .call(d3.axisLeft(y));

   var bar = g.selectAll(".bar")
        .data(data)

    bar.exit().remove()

    bar.enter().append("rect")
        .style("fill", function(d,i) { return color(i); })
        .attr("class", "bar")
        .on("mousemove", function(d){
            tooltip
              .style("left", d3.event.pageX - 50 + "px")
              .style("top", d3.event.pageY - 70 + "px")
              .style("display", "inline-block")
              .html((d.label) + "<br>" + (d.value));
        })
        .on("mouseout", function(d){ tooltip.style("display", "none");})
        .transition()
        .duration(500)
        .ease(d3.easeLinear)
        .attr("x", 0)
        .attr("height", y.bandwidth())
        .attr("y", function(d) { return y(d.label); })
        .attr("width", function(d) { return x(d.value); })

        d3.selectAll(".bar").on("click", function(d) {
                      if(d.label == 'Male' || d.label == 'Female' || d.label == 'Both Sexes'){
                        console.log("gender");
                        d3.selectAll(".genderspan").html(d.label);
                        changeAgeByGender(d.label);
                      }
                      else{
                        d3.selectAll(".agespan").html(d.label);
                        changeGenderByAge(d.label);
                      }
                    });

}

  function change() {
        d3.selectAll(".agespan").html('All Ages');
    $.getJSON($SCRIPT_ROOT + '/getAgeGroupData', {race : $('input[name="filter"]:checked').val(),year:$('input[name="sliderYear"]').val()}, function(d) { horbar1(d,"#barAge");});
    $.getJSON($SCRIPT_ROOT + '/getGenderData', {race : $('input[name="filter"]:checked').val(),year:$('input[name="sliderYear"]').val()}, function(d) { horbar1(d,"#barGender");});
  }

  function changeGenderByAge(age) {
    $.getJSON($SCRIPT_ROOT + '/getGenderDataByAge', {race : $('input[name="filter"]:checked').val(),year:$('input[name="sliderYear"]').val(),age:age}, function(d) { horbar1(d,"#barGender");});
  }

  function changeAgeByGender(gender) {
    $.getJSON($SCRIPT_ROOT + '/getAgeGroupDataByGender', {race : $('input[name="filter"]:checked').val(),year:$('input[name="sliderYear"]').val(),gender:gender}, function(d) { horbar1(d,"#barAge");});
  }