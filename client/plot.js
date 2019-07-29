
var value={};
// 2. Use the margin convention practice 
var margin = {top: 10, right: 160, bottom: 100, left: 50}
//   , width = window.innerWidth - margin.left - margin.right // Use the window's width 
//   , height = window.innerHeight - margin.top - margin.bottom; // Use the window's height
width = 1000;
height = 400;

d3.select("svg")
  .append("text")
  .text("Upload the data file to generate plot")
  .attr("x","50%")
  .attr("y","50%")
  .attr("dominant-baseline","middle")
  .attr("text-anchor","middle")

function draw(vals,hex){
  // The number of datapoints
  var n = vals.length;
  
  // 5. X scale will use the index of our data
  var xScale = d3.scaleLinear()
      .domain([0, n-1]) // input
      .range([0, width]); // output
  
  // 6. Y scale will use the randomly generate number 
  var yScale = d3.scaleLinear()
      .domain([Math.min(...vals), Math.max(...vals)]) // input 
      .range([height, 0]); // output 
  
  // 1. Add the SVG to the page and employ #2
  var svg = d3.select("body").select("svg")
    .attr('viewBox',`0 0 ${width + margin.left + margin.right} ${height + margin.top + margin.bottom}`)
    .append("g")
    .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

  // 3. Call the x axis in a group tag
  svg.append("g")
    .attr("class", "x axis")
    .attr("transform", "translate(0," + height + ")")
    .call(d3.axisBottom(xScale)); // Create an axis component with d3.axisBottom

  // 4. Call the y axis in a group tag
  svg.append("g")
    .attr("class", "y axis")
    .call(d3.axisLeft(yScale)); // Create an axis component with d3.axisLeft

  // 7. d3's line generator
  var line = d3.line()
      .x(function(d, i) { return xScale(i); }) // set the x values for the line generator
      .y(function(d) { return yScale(d.y); }) // set the y values for the line generator 
      .curve(d3.curveMonotoneX) // apply smoothing to the line
  
  // 8. An array of objects of length N. Each object has key -> value pair, the key being "y" and the value is a random number
  // var dataset = d3.range(n).map(function(d) { return {"y": d3.randomUniform(1)() } })
  let dataset=[];
  for (let i =0 ;i<vals.length;i++){
    dataset.push({y:vals[i]});
  }
  // 9. Append the path, bind the data, and call the line generator 
  svg.append("path")
  .datum(dataset) // 10. Binds data to the line 
  .attr("class", "line") // Assign a class for styling 
  .attr("d", line); // 11. Calls the line generator 

  // 12. Appends a circle for each datapoint 
  svg.selectAll(".dot")
  .data(dataset)
  .enter().append("circle") // Uses the enter().append() method
  .attr("class", "dot") // Assign a class for styling
  .attr("cx", function(d, i) { return xScale(i) })
  .attr("cy", function(d) {return yScale(d.y) })
  .attr("r", 4)
  .on('mouseover',(d,i)=>{
    tooltip.style("visibility", "visible")
      .attr("x", xScale(i)+3)
      .attr("y", yScale(d.y)+3)
      .attr("xlink:href",`img/${hex}/${i}.png`);
  })
  .on('mouseout',(d,i)=>{
      tooltip.style("visibility", "hidden");
  })

  let tooltip = svg
    .append("image")
    .style("visibility", "hidden")
}

function update_svg(vals){
  console.log(vals)
  $('svg').empty();
  value = vals;
  draw(vals.vals,vals.hex);
}

$('#nd2_form')
  .ajaxForm({
    success: update_svg,
  });

$('#tif_form')
  .ajaxForm({
    success: update_svg,
  });

function exportCSV(){
  let csv = 'Time,Value\n';
  console.log(value.vals)
  for (i=0;i<value.vals.length;i++){
    csv+=i;
    csv+=',';
    csv+=value.vals[i];
    csv+='\n'
  }

  console.log(csv);
  var hiddenElement = document.createElement('a');
  hiddenElement.href = 'data:text/csv;charset=utf-8,' + encodeURI(csv);
  hiddenElement.target = '_blank';
  hiddenElement.download = 'value.csv';
  hiddenElement.click();
}