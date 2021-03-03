function active_incidents() {
  var data = null;

  var xhr = new XMLHttpRequest();
  xhr.withCredentials = false;

  xhr.addEventListener("readystatechange", function () {
    if (this.readyState === this.DONE) {
      var active_fires = JSON.parse(this.responseText);
      document.getElementById("activefires").innerHTML = active_fires.length;
    }
  });
  xhr.open("GET", "http://45.63.15.162:8000/data/active_incidents.json", true);
  xhr.send(data);
}

function incidents() {
  var data = null;

  var xhr = new XMLHttpRequest();
  xhr.withCredentials = false;

  xhr.addEventListener("readystatechange", function () {
    if (this.readyState === this.DONE) {
      var response = JSON.parse(this.responseText);
      var startDate = new Date("2020-01-01");
      var endDate = new Date("2020-12-31");
      var fires_2020_data = fires_2020(startDate, endDate, response);

      var worst_in_2020 = worst_fire_2020(fires_2020_data);

      //    fires_2020_data.forEach(element => {
      //        console.log(element.acres);
      //    });

      document.getElementById("firesin2020").innerHTML = fires_2020_data.length;
      document.getElementById(
        "worst_fire_2020_actres"
      ).innerHTML = worst_fire_2020_actres(fires_2020_data);

      document.getElementById("worst_in_2020").innerHTML =
        "<b>" +
        worst_in_2020.name +
        " </b> x" +
        worst_in_2020.acres +
        "  acres burned";
      var worst_by_countr = worst_afected_country(fires_2020_data);
      document.getElementById("worst_affected_country_fires").innerHTML =
        "<b>" +
        worst_by_countr.worst_by_fires["country"] +
        "</b> x " +
        worst_by_countr.worst_by_fires.fires +
        " fires";
      document.getElementById("worst_affected_country_acres").innerHTML =
        "<b>" +
        worst_by_countr.worst_by_acres["country"] +
        "</b> x " +
        worst_by_countr.worst_by_acres.acres +
        " acres";
    }
  });

  xhr.open("GET", "http://45.63.15.162:8000/data/incidents_2020.json", true);

  xhr.send(data);
}

function fires_2020(startDate, endDate, fires) {
  var filteredData = fires.filter((a) => {
    var date = new Date(a.startedDate);

    return date >= startDate && date <= endDate;
  });
  return filteredData;
}

function worst_fire_2020(data) {
  console.log(data);
  var arr_2020 = [];

  data.forEach((element) => {
    console.log(element.acres);
    if (element.acres == "") {
      element.acres = 0;
      // element.acres=parseFloat(element.acres);
    } else {
      element.acres = parseFloat(numeral(element.acres).value());
    }

    arr_2020.push(element);

    // console.log(element.acres+'--'+Number.isInteger(element.acres));
  });

  arr_2020.sort((a, b) => b.acres - a.acres);
  console.log(arr_2020);
  return arr_2020[0];
}

function worst_fire_2020_actres(data) {
  // console.log(data);
  // var arr_2020 = [];
  var total_actres = 0;
  data.forEach((element) => {
    // console.log(element.acres);
    if (element.acres == "") {
      element.acres = 0;
      // element.acres=parseFloat(element.acres);
    } else {
      element.acres = parseFloat(
        element.acres.toString().replace(/[^\d\.\-]/g, "")
      );
    }

    // arr_2020.push(element);

    // console.log(element.acres+'--'+Number.isInteger(element.acres));
    total_actres += element.acres;
  });

  return total_actres;
}

function worst_afected_country(fires) {
  var fires_2020_groupedarr = groupby(fires);
  // console.log(fires_2020_groupedarr);
  var arr = [];

  Object.keys(fires_2020_groupedarr).forEach(function (key) {
    // do something with obj[key]
    // console.log(key);
    var firecount = 0;
    var acrecount = 0;

    for (let i = 0; i < fires_2020_groupedarr[key].length; i++) {
      const country = fires_2020_groupedarr[key][i];
      // console.log(country);

      var acre = country.acres.toString();
      if (acre == null || acre == "") {
        acre = 0;
      } else {
        acre = parseFloat(acre.replace(/[^\d\.\-]/g, ""));
      }
      acrecount += acre;
    }

    arr.push({
      country: key,
      fires: fires_2020_groupedarr[key].length,
      acres: acrecount,
    });
  });
  // console.log(arr);

  return {
    worst_by_fires: arr.sort((a, b) => b.fires - a.fires)[0],
    worst_by_acres: arr.sort((a, b) => b.acres - a.acres)[0],
  };
}

function groupby(fires) {
  return fires.reduce((r, a) => {
    r[a.counties] = [...(r[a.counties] || []), a];
    return r;
  }, {});
}

// });

function mainfunction() {
  incidents();
  active_incidents();
}
mainfunction();