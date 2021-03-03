function getalldata_terrorism(data) {
  var labels = Object.keys(data);
  var bulk = [];

  labels.forEach((label) => {

    data[label].forEach((terror) => {
      var total_death = 0;
      var death2 = 0;
      var dead1 = 0;
        //  ++i;

      if ("perpetrators" in terror) {
        terror.perpetrator = terror.perpetrators;
      }
      if (terror.perpetrator === undefined) {
        terror.perpetrator = "unknown";
      }
      
      if ("dead2" in terror) {
        death2 = parseInt(terror.dead2);
      }
      if ("dead1" in terror) {
        dead1 = parseInt(terror.dead1);
      }
      total_death += dead1 + death2;
      var date = moment(terror.date + " " + label);
      terror.year = label;
      terror.month = moment(terror.date + " " + label).format("MMMM");
      terror.fulldate = moment(terror.date + " " + label).format("YYYY-MM-DD");
      terror.total_death = total_death;
      if (terror.country ==
          "Iraq The 2007 Yazidi communities bombings in northern Iraq kills nearly 800; this the Iraq War's most deadly car bomb attack during the period of major American combat operations") {
   terror.country="iraq";
          }
      if (terror.description===undefined) {
        terror.description=terror.details;
      }
var split = terror.description.split(":");

      if (terror.year>=2010) {
     
        terror.maker=split[0];
     
      }else{
        terror.maker=terror.location;
      }
      if (terror.year>2020) {
        alert("data error");
      }

      if (isNaN(terror.latitude) || isNaN(terror.longitude)) {
        console.log(terror.year);
      }
  terror.cords = new google.maps.LatLng({
    lat: parseFloat("" + terror.latitude),
    lng: parseFloat(terror.longitude),
  }); 
      // console.log(apn);
      bulk.push(terror);
    });
  });
 
  return bulk;
}

function groupbyyear(attacks) {
  return attacks.reduce((r, a) => {
    r[a.year] = [...(r[a.year] || []), a];
    return r;
  }, {});
}
function groupby_trrgroup(data) {
  return data.reduce((r, a) => {
    r[a.perpetrator] = [...(r[a.perpetrator] || []), a];
    return r;
  }, {});
}
function groupby_trrtype(data) {
  return data.reduce((r, a) => {
    r[a.type] = [...(r[a.type] || []), a];
    return r;
  }, {});
}

function addtotag(id, content) {
  if (document.getElementById(id)) {
    document.getElementById(id).innerHTML = content;
  } else {
    console.log(id + "not in dom");
  }
}

function getuniquecountries(data, year) {
  var array = [];
  data.forEach((element) => {
    var country = element.country;

    if (!country.includes("America")) {
      array.push({
        counties: country,
      });
    }
  });
  var groupedcountry = groupby_countries(array);
  
  return groupedcountry;
}

function getnoofdeaths(data) {
  var nofdeaths = 0;

  data.forEach((element) => {
    var death2 = 0;
    if ("dead2" in element) {
      death2 = parseInt(element.dead2.replace(/[^\d\.\-]/g, ""));
    }
    nofdeaths += parseInt(element.dead1.replace(/[^\d\.\-]/g, "")) + death2;
  });

  console.log(nofdeaths);
  return nofdeaths;
}

function getnoofdeaths2019(data) {
  var nofdeaths = 0;
  var arr = [];
  data.forEach((element) => {
    var death2 = 0;

    arr.push(element.dead1);
    nofdeaths += parseInt(element.dead1);
  });

  return nofdeaths;
}

function groupby_countries(fires) {
  return fires.reduce((r, a) => {
    r[a.counties] = [...(r[a.counties] || []), a];
    return r;
  }, {});
}
function getworstaffectedcity(data) {
  var array = [];
  data.forEach((element) => {
    var country = element.location.split(", ")[1];
    if (country === undefined) {
    } else {
      country = element.location;
    }

    if (country == "") {
    } else {
      var death2 = 0;
      if ("dead2" in element) {
        death2 = parseInt(element.dead2.replace(/[^\d\.\-]/g, ""));
      }
      array.push({
        counties: country,
        deaths: parseInt(element.dead1) + death2,
      });
    }
  });

  var grouped = groupby_countries(array);
  var countries = Object.keys(grouped);
  // console.log();
  var country_values = [];
  countries.forEach((element) => {
    var count = 0;
    for (let i = 0; i < grouped[element].length; i++) {
      const country = grouped[element][i];
      count += country.deaths;
    }

    if (count != 0) {
      country_values.push({
        country: element,
        count: count,
      });
    }
  });
  return country_values.sort((a, b) => b.count - a.count)[0];
}

function getworseincident(data) {
  var arr = [];
  console.log(data);
  data.forEach((element) => {
    var death2 = 0;

    if ("dead2" in element) {
      death2 = parseInt(element.dead2.replace(/[^\d\.\-]/g, ""));
    }
    element.total_death = parseInt(element.dead1) + death2;
    arr.push(element);
  });

  return arr.sort((a, b) => b.total_death - a.total_death)[0];
}

function add_class(element, value) {
  document.getElementById(element).classList.add(value);
}

function getworseaffectedcountry(data) {
  var array = [];
  data.forEach((element) => {
    var country = element.country;

    if (country == "") {
    } else {
      var death2 = 0;
      if ("dead2" in element) {
        death2 = parseInt(element.dead2.replace(/[^\d\.\-]/g, ""));
      }
      array.push({
        counties: country,
        deaths: parseInt(element.dead1) + death2,
      });
    }
  });

  var grouped = groupby_countries(array);
  var countries = Object.keys(grouped);

  var country_values = [];
  countries.forEach((element) => {
    var count = 0;
    for (let i = 0; i < grouped[element].length; i++) {
      const country = grouped[element][i];

      count += country.deaths;
    }

    if (count != 0) {
      country_values.push({
        country: element,
        count: count,
      });
    }
  });

  return country_values.sort((a, b) => b.count - a.count)[0];
}

function getalldata_intoarr(data_arr, year_get) {
  var new_data = [];
  var years = Object.keys(data_arr);

  for (let i = 0; i < years.length; i++) {
    const year = years[i];

    if (year == year_get) {
      data_arr[year].forEach((element) => {
        element.year = year;
        new_data.push(element);
      });
    }
  }

  return new_data;
}
function get_data_byyear(data, year) {
  var startDate = moment(year + "-01-01").toDate();
  var endDate = moment(year + "-" + moment().format("MM-DD")).toDate();

  var filteredData = data.filter((a) => {
    var date = new Date(a.date + " " + year);

    return date >= startDate && date <= endDate;
  });
  return filteredData;
}

function getlimitedval(data, count) {
  // var newdata=data.slice(count,data.length);
  var nwdata = [];
  var i = 0;
  data.forEach((element) => {
    if (i <= count) {
      nwdata.push(element);
    }
    ++i;
  });
  return nwdata;
}

//   --------------chart
function createselection(id) {
  const choices = new Choices(document.getElementById(id), {
    removeItemButton: true,
  });
  return choices;
}
function createchart(id) {
  var ctx = document.getElementById(id);
  var myChart_data = new Chart(ctx, {
    type: "line",
    data: {
      labels: [],
      datasets: [],
    },
    options: {
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
            type: "time",
            distribution: "series",

            time: {
              unit: "year",
              parser: "YYYY",
              tooltipFormat: "YYYY",
            },
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

    function groupbyconflict(attacks) {
      return attacks.reduce((r, a) => {
        //   console.log(r);
        if ("partOf" in a) {
           a.partOf = a.partOf.toLowerCase(); 
          r[a.partOf] = [...(r[a.partOf] || []), a];
        }
        return r;
      }, {});
    }

     function groupbycountry(attacks) {
       return attacks.reduce((r, a) => {
         r[a.country] = [...(r[a.country] || []), a];
         return r;
       }, {});
     }
function renderChart(data_set, labels = [], myChart_data) {
 
  myChart_data.data.datasets = data_set;
  myChart_data.data.labels = labels;
  myChart_data.update();
}
Array.prototype.sum = function (prop) {
  var total = 0;
  for (var i = 0, _len = this.length; i < _len; i++) {
    total += this[i][prop];
  }
  return total;
};
Array.prototype.sample = function () {
  return this[Math.floor(Math.random() * this.length)];
};
