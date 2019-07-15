
var vals = [78622.8515625, 48068.3515625, 79585.80078125, 120295.6484375, 111129.1015625, 40857.66796875, 55177.8359375, 120052.44921875, 136603.5, 69246.453125, 46621.05078125, 93774.56640625, 108917.30078125, 62260.9140625, 81457.19921875, 95606.30078125, 114946.3984375, 68704.953125, 79518.0859375, 101699.5859375, 99605.55078125, 48839.5, 74582.3984375, 92215.55078125, 79097.78125, 41175.515625, 78529.03125, 95554.8984375, 85655.3515625, 65018.8984375, 116035.8515625, 112636.33203125, 70432.5859375, 92882.44921875, 105976.30078125, 116087.6640625, 61522.953125, 72670.75, 109459.0, 113263.3515625, 56158.796875, 87028.94921875, 94363.3828125, 92029.3515625, 28646.69921875, 21327.80078125, 28012.6484375, 92682.94921875, 31825.734375, 100716.9140625, 100079.25, 77917.80078125, 44412.5, 77049.234375, 98450.3984375, 80284.5, 41938.015625, 52724.05078125, 54474.546875, 92322.8984375, 47862.6484375, 93434.015625, 104675.8828125, 108363.5, 48202.0, 97103.953125, 115002.25, 118466.33203125, 47900.765625, 48889.3984375, 69647.78125, 83825.30078125];
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
