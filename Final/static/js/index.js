 width = 500;
height = 400;
var margin = {top: 20, right: 20, bottom: 30, left: 30};
var parseTime = d3.timeParse("%Y");
dataset = {}

var svg = d3.select("#third")
            .append("svg")
            .attr("width",width  + margin.left + margin.right )
            .attr("height",height + margin.top + margin.bottom);   

var svg4 = d3.select("#rxDeathDiv")
            .append("svg")
            .attr("width",width  + margin.left + margin.right )
            .attr("height",height + margin.top + margin.bottom);  

$.getJSON($SCRIPT_ROOT + '/bubbleData', {}, function(d) { dataset["children"]=d; drawBubble(dataset);});
/*
Bubble Chart data
*/




function drawBubble(dataset){
  console.log("A");
  console.log(dataset);
console.log("BIGGGGG");
 var diameter = 500;
    var color = d3.scaleOrdinal(d3.schemeCategory20);

    var bubble = d3.pack(dataset)
            .size([diameter, diameter])
            .padding(1.5);
    var svg = d3.select("#stateBubbleDiv")
            .append("svg")
            .attr("width", 600)
            .attr("height", 550)
            .attr("class", "bubble");

    var nodes = d3.hierarchy(dataset)
            .sum(function(d) { return d.percent_opioid_claim; });

    var node = svg.selectAll(".node")
            .data(bubble(nodes).descendants())
            .enter()
            .append("g")
            .attr("class", "node")
            .attr("transform", function(d) {
                return "translate(" + d.x + "," + d.y + ")";
            });

    node.append("title")
            .text(function(d) {
                return d.data.state_abr + ":" + d.data.percent_opioid_claim;
            });

    node.append("circle")
            .attr("r", function(d) {
                return d.data.percent_opioid_claim*6.5;
            })
            .style("fill", function(d) {
                return color(d.data.state_abr);
            });

    node.append("text")
            .attr("dy", ".3em")
            .style("text-anchor", "middle")
            .text(function(d) {
                return d.data.state_abr + ":" + d.data.percent_opioid_claim+"%";
            });

    d3.select(self.frameElement)
            .style("height", diameter + "px");

    svg.append("text")
      .attr("x", 100)             
      .attr("y", 30)
      .attr("text-anchor", "middle")  
      .style("font-size", "16px") 
      .style("fill","black")
      .style("text-decoration", "underline")  
      .text("Percentage of Opioid Claims");

}

/* Loading rxDeathYear.csv file*/
d3.csv("../static/data/copyOfrxDeathYear.csv")
   .row(function(d) {
    // for each row of the data, create an object with these properties...
    return {
      PC1: +d.rx,
      PC2: +d.deaths/1000,
      year  : parseTime(d.year)
    };
  })
  .get(function(error, fileData) {
    if (!error) {
      console.log("Successfully Loaded - copyOfrxDeathYear.csv")
       drawLine(fileData);
      }
     else {
      console.log("Errorcdjkhejvefjhvekjfkjerhfjkrhfjdwfj3h");
    }
  });







function drawLine(pca2){

var xScale = d3.scaleLinear()
            .domain([d3.min(pca2, function(d){return d.PC1;}), d3.max(pca2, function(d){return d.PC1 ;})])
            .range([margin.left,width-margin.right]);

var yScale = d3.scaleLinear()
            .domain([d3.min(pca2, function(d){return d.PC2;}), d3.max(pca2, function(d){return d.PC2;})])
            .range([height,margin.top]);

    svg4.append("g")
      .attr("class", "axis")
      .attr("transform", "translate(0," + height + ")")
      .call(d3.axisBottom(xScale));
     
     svg4.append("g")
      .attr("transform", "translate(30," + 0 + ")")
      .call(d3.axisLeft(yScale));

      svg4.selectAll("dot")
      .data(pca2)
      .enter().append("circle")
      .attr("r", 3)
      .style("fill","red")
      .attr("cx", function(d) { return xScale(d.PC1); })
      .attr("cy", function(d) { return yScale(d.PC2); });
        
       svg4.append("text")
      .attr("x", 100)             
      .attr("y", 30)
      .attr("text-anchor", "middle")  
      .style("font-size", "12px") 
      .style("fill","black")
      .style("text-decoration", "underline")  
      .text("Deaths (In Thousands)");

      svg4.append("text")
      .attr("x", (width / 2)-10)             
      .attr("y", (height)+margin.bottom+15)
      .attr("text-anchor", "middle")  
      .style("font-size", "12px") 
      .style("fill","black")
      .style("text-decoration", "underline")  
      .text("Rx - Prescription (In Million dollars)");
}

drawViz();
function drawViz(path){
var parseDate = d3.timeParse("%Y");

var x = d3.scaleTime().range([0, width]),
    y = d3.scaleLinear().range([height, 0]),
    z = d3.scaleOrdinal(d3.schemeCategory10);

var stack = d3.stack();

var area = d3.area()
    .x(function(d, i) { return x(d.data.year); })
    .y0(function(d) { /*console.log("y0 %s",d[0]);*/ return y(d[0]); })
    .y1(function(d) { /*console.log("y1 %s",d[1]);*/ return y(d[1]); });

var g = svg.append("g")
    .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

      path_cause = "../static/data/copyOfYearcauseDeath.csv";
      path_age = "../static/data/copyOfYearAgeGroupDeath.csv";
      path_gender = "../static/data/copyOfYearGenderDeath.csv";
      path_race = "../static/data/copyOfYearRaceDeath.csv";
       final_path = "../static/data/copyOfYearcauseDeath.csv";
      if(path ==1){
        final_path = path_cause;  
      }
      else if(path==2){
        final_path = path_age;
      }
      else if (path==3){
        final_path = path_gender;
      }
      else if (path == 4){
        final_path = path_race;
      }

      d3.csv(final_path, type,  function(error, data){ 
        if (error) throw error;

        var keys = data.columns.slice(1);

         //console.log(keys);

        x.domain(d3.extent(data, function(d) { return d.year; }));
        z.domain(keys);
        stack.keys(keys);

        var layer = g.selectAll(".layer")
          .data(stack(data))
          .enter().append("g")
            .attr("class", "layer");

        layer.append("path")
            .attr("class", "area")
            .style("fill", function(d) {return z(d.key); })
            .attr("d", area);

        layer.filter(function(d) { return d[d.length - 1][1] - d[d.length - 1][0] > 0.01; })
          .append("text")
            .attr("x", width-6)
            .attr("y", function(d) { return y((d[d.length - 1][0] + d[d.length - 1][1]) / 2); })
            .attr("dy", ".35em")
            .style("font", "10px sans-serif")
            .style("text-anchor", "end")
            .text(function(d) { return d.key; });

        g.append("g")
            .attr("class", "axis axis--x")
            .attr("transform", "translate(0," + height + ")")
            .call(d3.axisBottom(x));

        g.append("g")
            .attr("class", "axis axis--y")
            .call(d3.axisLeft(y).ticks(10, "%"));
      });

function type(d, i, columns) {
  //console.log(d);
  d.year = parseDate(d.year);
  total = 0;

  for (var i = 1, n = columns.length; i < n; ++i)
  {
   
   total = total+( +d[columns[i]]);
   //d[columns[i]] = d[columns[i]] / 100;

  }

  //console.log(total);

  for (var i = 1, n = columns.length; i < n; ++i)
  {
   
   //console.log(d[columns[i]])

   d[columns[i]] = d[columns[i]]/total;

   //d[columns[i]] = d[columns[i]] /;

  }
  //console.log(d);
  return d;
  }

 } // drawViz ends here  