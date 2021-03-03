var animatedchart = null;
var interval = null;

window.animatedchart = createchart_default("animated-countrychart");
loaddefaultdata();
// console.log("animated");
// console.log(window.animatedchart);

function loadanimateddata() {
  var data = null;

  var xhr = new XMLHttpRequest();
  xhr.withCredentials = false;

  xhr.addEventListener("readystatechange", function () {
    if (this.readyState === this.DONE) {
      var res = JSON.parse(this.responseText);

      var year = moment().format("YYYY");
      var alldata = getalldata_terrorism(res);
      var topcountries = get_topcountries(alldata);
      var gorupdeyear = alldata.reduce((r, a) => {
        r[a.year] = [...(r[a.year] || []), a];
        return r;
      }, {});
      var groupkeys = Object.keys(gorupdeyear);
      var minyear = 1970;
      console.log(minyear);
      var maxyear = year;
      interval = setInterval(() => {
        if (gorupdeyear[minyear] === undefined) {
        } else {
          if (minyear == year) {
            clearInterval(interval);
            fun_getchartdata(gorupdeyear[year], year,topcountries);
          } else {
            fun_getchartdata(gorupdeyear[minyear], minyear,topcountries);
          }
        }
        // alert(minyear);
        ++minyear;
      }, 2000);
      groupkeys.forEach((key) => {
        // var getchartdata = fun_getchartdata(gorupdeyear[key], key);
      });
    }
  });

  xhr.open("GET", "http://45.63.15.162:8000/data/terrorist_incidents.json");

  xhr.send(data);
}
function get_topcountries(data) {

  var gorupdcountry = data.reduce((r, a) => {
    r[a.country] = [...(r[a.country] || []), a];
    return r;
  }, {});
  var keys=Object.keys(gorupdcountry);


  var dataset_1st=[];
  var countries=[];
  keys.forEach(key => {
    // total_death
dataset_1st.push({
  country:key,
  death:gorupdcountry[key].sum('total_death')
  });



  });

dataset_1st.sort((a, b) => b.death - a.death);
var i=0;
dataset_1st.forEach((el) => {
++i;
if (i<=30) {
  countries.push(el.country);
  if (i!=17) {
    
  }
}

});
  
return countries;

}

function loaddefaultdata() {
  var data = null;

  var xhr = new XMLHttpRequest();
  xhr.withCredentials = false;

  xhr.addEventListener("readystatechange", function () {
    if (this.readyState === this.DONE) {
      var res = JSON.parse(this.responseText);

      var year = moment().format("YYYY");
      var alldata = getalldata_terrorism(res);
      var topcountries = get_topcountries(alldata);
      var gorupdeyear = alldata.reduce((r, a) => {
        r[a.year] = [...(r[a.year] || []), a];
        return r;
      }, {});
      var getchartdata = fun_getchartdata(
        gorupdeyear[year],
        year,
        topcountries
      );
    }
  });

  xhr.open("GET", "http://45.63.15.162:8000/data/terrorist_incidents.json");

  xhr.send(data);
}
function fun_getchartdata(data, year,include_countries) {
  var country = data.reduce((r, a) => {
    r[a.country] = [...(r[a.country] || []), a];
    return r;
  }, {});
   console.log(include_countries);
  // include_countries;
  var labels = Object.keys(country);
  var dataset = [];
  var i = 0;
  labels.forEach((label) => {
    ++i;
    include_countries.forEach((incount) => {
if (label == incount) {

  var data_country = [];
  var death = 0;

  country[label].forEach((element) => {
    death += element.total_death;
  });

  data_country.push({
    x: label,
    y: death,
  });
  dataset.push({
    label: "" + year + "-" + label,
    data: data_country,
    backgroundColor: getcolors()[i],

    borderColor: "blue",
    barThickness: 30,

    pointRadius: 2,
    fill: true,
    lineTension: 0,
    borderWidth: 0,
  });
}


    });

  });
  console.log(dataset);

  renderChart(dataset, include_countries, window.animatedchart);
  //  console.log(data_country);
}
function createchart_default(id) {
  var ctx = document.getElementById(id);
  var myChart_data = new Chart(ctx, {
    type: "bar",
    data: {
      labels: [],
      datasets: [],
    },
    options: {
      animation: {
        tension: {
          duration: 1000,
          easing: "linear",
          from: 1,
          to: 0,
          loop: true,
        },
      },
      legend: {
        display: true,
        onHover: function (event, legendItem) {
          var options = this.options || {};
          var hoverOptions = options.hover || {};
          var ci = this.chart;
          hoveredDatasetIndex = legendItem.datasetIndex;
          ci.updateHoverStyle(
            ci.getDatasetMeta(hoveredDatasetIndex).data,
            hoverOptions.mode,
            true
          );
          ci.render();
        },
      },
      //   hover: {
      //     mode: "dataset",
      //   },

      scales: {
        xAxes: [
          {
            // type: "time",
            // distribution: "series",
            // time: {
            //   unit: "year",
            //   parser: "YYYY",
            //   tooltipFormat: "YYYY",
            // },
          },
        ],
        yAxes: [
          {
            ticks: {
              stepSize: 10,
            },
          },
        ],
      },
      tooltips: {
        intersect: false,
        mode: "index",
        callbacks: {
          label: function (tooltipItem, myData) {
            var label = myData.datasets[tooltipItem.datasetIndex].label || "";
            if (label) {
              label += ": ";
            }
            label += parseInt(
              myData.datasets[tooltipItem.datasetIndex].data[tooltipItem.index]
                .y
            );

            return label;
          },
        },
      },
    },
  });
  return myChart_data;
}
