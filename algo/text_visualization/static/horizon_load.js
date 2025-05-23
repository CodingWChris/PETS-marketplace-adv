var horizons_load = function(){ 
    //variables accessible to the rest of the functions inside SmallMultiples
    
    // width = 500;
    // height = 300;
    // band_height = 25;
    // hmargin = {
    //   top: 2
    // };
    
    // set the width of the chart to be % of the father container width 
    function getContainerWidth() {
      var container = document.getElementById('vis-horizon'); // 'vis-horizon' inherents the width of the father container 'full-width' 
      if (container) {
          var parentWidth = container.parentNode.clientWidth;
          // Account for padding (40px total from both sides)
          return parentWidth - 40;
      }
      return Math.min(800, window.innerWidth * 0.95);
  }

    // Calculate dimensions based on container
    var availableWidth = getContainerWidth();

    // Set margins as a percentage of available width
    var marginPercent = 0.03; // 3% margin
    var margin = {
        left: Math.floor(availableWidth * marginPercent),
        right: Math.floor(availableWidth * marginPercent)
    };

    // Width is container width minus margins
    width = availableWidth - margin.left - margin.right;



    // var windowWidth = window.innerWidth;
    // var marginPercent = 0.05; // 5% margin
    // var margin = {
    //   left: Math.floor(windowWidth * marginPercent), 
    //   right: Math.floor(windowWidth * marginPercent)
    // }; 
    
    // // Limit width and add margins - at most 80% of window width
    // width = Math.min(windowWidth * 0.8, windowWidth - margin.left - margin.right); 
    
    height = window.innerHeight;
    band_height = 100; // height of each band
    hmargin = {
      top: 2
    };

    var chart = d3.horizon()
      .width(width)
      .height(band_height)
      .mode("offset")
      .interpolate("basis")
      ;
      
    
    func_horizonchart = function init(selection){  

        var svg = selection.append("svg")
          .attr("width", width )
          .attr("height", height)
          .style("margin", "0 auto")
          .style("display", "block");;


        // INSERT
        var tableContainer = d3.select("#words-table-container")
          .attr("class", "words-table-container")
          .style("width", width + "px")
          .style("margin", "20px auto")
          .style("max-height", "300px")
          .style("overflow-y", "auto")
          .style("border", "1px solid #eee")
          .style("border-radius", "5px")
          .style("padding", "10px")
          .style("display", "none")
          // .style("opacity", "0")  // intially hidden
          // .style("transition", "opacity 0.3s ease"); // fade-in effect

        // table title
        tableContainer.append("h3")
          .text("Contributing Words by Sentiment Category")
          .style("margin", "0 0 10px 0")
          .style("text-align", "center");

        // create a table element
        var table = tableContainer.append("table")
          .attr("class", "words-table")
          .style("width", "100%")
          .style("border-collapse", "collapse")
          .style("font-family", "Arial, sans-serif");

        // add a header row
        var thead = table.append("thead");
        thead.append("tr")
          .selectAll("th")
          .data(["Sentiment Category", "Contributing Words"])
          .enter()
          .append("th")
          .text(function(d) { return d; })
          .style("padding", "8px")
          .style("text-align", "left")
          .style("border-bottom", "2px solid #ddd");

        // add a body to the table
        table.append("tbody")
          .attr("id", "words-table-body");

        // END INSERT

        d3.json(dir+"sentiment_converted.json", function(error, data) {

          min=Infinity;
          max=0;

          // TODO: change it to make the value have addtional information: list of words 
          data.forEach(function(d,i){
              var list = d.values.map(function(c){ 
                return c[1];   // [category name , date and counts] -> get date and counts
              });            
              var val = d3.extent(list);
              if(val[0]<min){min =val[0];}
              if(val[1]>max){max = val[1];}

              // INSERT
              if (!d.words) {
                d.words = d.values.map(function(v) {
                    return [v[0], []];
                });
              }
              //console.log(min, max, d.name, val);
          });

          
          // How many max bands?
          if(max<chart.maxY()){chart.maxBands(1)}
          // max for yScale
          chart.maxY(max);
          

          /** ---
          Create a div and an SVG element for each element in
          our data array. Note that data is a nested array
          with each element containing another array of 'values'
          */

          g = svg.selectAll("g").data(data);

          // Adding chart title
          svg.append("text")
            .text("Sentiment Categories")
            .attr("y", "10")
            .attr("dy", ".75em")
            .attr("class", "bold-legend")
            .style("text-anchor", "end")
            .attr("x", width-25);
          
          // Adding the data points 
          g.enter()
            .append("g")
            .attr("class", "h-group")
            .attr("transform", function(d,i){
              return "translate("+ [0, 15+i*(band_height + hmargin.top)]+ ")";
            });
          g.call(chart);

          // showing the date   
          svg.append("text")
            .text("date")
            .attr("id", "date-caption")
            .attr("class", "bold-legend")
            .attr("text-anchor", "middle")
            .style("pointer-events", "none")
            .attr("x", width*0.7)
            .attr("y", height/2);

        });

        // TODO: add a function to update the table showing the words in the selected band
    }

    return func_horizonchart;
}