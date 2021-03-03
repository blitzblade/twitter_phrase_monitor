// Create the script tag, set the appropriate attributes
var script = document.createElement("script");
script.src =
  "https://maps.googleapis.com/maps/api/js?key=AIzaSyAgDf2DBQwy33XYxD7jKmO0AIo5TT06Q0U&callback=initMap";
script.defer = true;
let resultsMap = null;
let geocoder = null;
let markers = [];
let intrvl = null;
let onanimation = false;
// Attach your callback function to the `window` object
window.initMap = function () {
  // JS API is loaded and available
  geocoder = new google.maps.Geocoder();
  //   alert("works");
  window.resultsMap = new google.maps.Map(
    document.getElementById("map"),
    mapparams(36.778259, -119.417931, 5)
  );
  mapfunc(resultsMap);
  //   getAjaxdata(resultsMap, geocoder);
};

// console.log(mapparams(51.4934, 0.0098, 2));

// Append the 'script' element to 'head'
document.head.appendChild(script);

function mapfunc(resultsMap) {
  var data = null;

  var xhr = new XMLHttpRequest();

  xhr.addEventListener("readystatechange", function () {
    if (this.readyState === this.DONE) {
      // console.log(this.responseText);
      var results = JSON.parse(this.responseText);

      var all_data = get_alldata(results);

      var all_data_bydate = all_data.reduce((r, a) => {
        r[a.startedDate] = [...(r[a.startedDate] || []), a];
        return r;
      }, {});
      // console.log(all_data_bydate);
      var alldates = Object.keys(all_data_bydate);
      document.getElementById("range").setAttribute("max", alldates.length);
      document.getElementById("range").value = 0;
      document.getElementById("json_val").value = JSON.stringify(all_data);

      genmap(all_data, resultsMap);
    }
  });

  xhr.open("GET", "http://45.63.15.162:8000/data/allyears_incidents.json");

  xhr.send(data);
}

function setMapOnAll() {
  for (let i = 0; i < window.markers.length; i++) {
    window.markers[i].setMap(null);
  }
}

function addMarker(location, map, label) {
  // Add the marker at the clicked location, and add the next-available label
  // from the array of alphabetical characters.
  var color = getcolors();
  var icn = {
    path: google.maps.SymbolPath.CIRCLE,
    scale: 10,
    fillColor: color.getRandom(),
    fillOpacity: 1,
    strokeWeight: 0.6,
    //  strokeColor: getcolors().sample(),
  };
  var icon = {
    url: "../marker.png", // url
    scaledSize: new google.maps.Size(25, 25), // scaled size
    origin: new google.maps.Point(0, 0), // origin
    anchor: new google.maps.Point(0, 0), // anchor
  };

  // console.log(getmarkericon());
  var marker = new google.maps.Marker({
    position: location,
    //  label: label.location,

    map: map,
    //  animation: google.maps.Animation.DROP,
    icon: icn,
    //  icon: getmarkericon(),
  });
  return marker;
}

function genmap(all_data, resultsMap) {
  var mkr = [];
  all_data.forEach((element) => {
    var latlng = new google.maps.LatLng(element.latitude, element.longitude);
    // console.log(latlng);

    if (
      element.latitude != 0 &&
      element.longitude != 0 &&
      element.year == 2020
    ) {
      mkr.push(addMarker(latlng, window.resultsMap, null));
      // addMarker(latlng, resultsMap,null);
    }

    //  console.log(addMarker(latlng, wresultsMap, null));
  });
  window.markers = mkr;
}

function animatebtn() {


      var all_data = getjsondata();
      var all_data_bydate = all_data.reduce((r, a) => {
        r[a.startedDate] = [...(r[a.startedDate] || []), a];
        return r;
      }, {});


      document.getElementById("pause-btn").removeAttribute('hidden');
      // console.log(all_data_bydate);
      var alldates = Object.keys(all_data_bydate);
      var i = parseInt(document.getElementById("range").value);
      window.onanimation=true;
      // setMapOnAll();
      window.intrvl = setInterval(() => {
        // console.log('aa');
        if (i > alldates.length || all_data_bydate[alldates[i]] === undefined) {
          clearInterval(window.intrvl);
          window.intrvl = null;
          window.onanimation = false;
          i = 0;
          document.getElementById("range").value = 0;


          genmap(all_data, window.resultsMap);
        } else {
          document.getElementById("range").value = i;

    setmarkersanimate(all_data_bydate[alldates[i]], window.resultsMap);
          // var el = document.getElementById("range");
          // el.onchange();

        }
        // console.log(all_data_bydate[alldates[i]]);
        ++i;
      }, getcaliforniainterval());
 
}

function setmarkersanimate(data, resultsMap) {
  var mkr = [];
  setMapOnAll();
  if (data.length > 0) {
    data.forEach((element) => {
      // console.log(element);
      var latlng = new google.maps.LatLng(element.latitude, element.longitude);
      if (element.latitude != 0 && element.longitude != 0) {
        mkr.push(addMarker(latlng, window.resultsMap, null));
        // addMarker(latlng, resultsMap,null);
      }
      document.getElementById("mapyear").innerHTML = element.startedDate;
    });
    window.markers = mkr;
    // console.log(mkr);
  }
}

document.getElementById('range').addEventListener("change", function (e) { 

clearInterval(window.intrvl);
document.getElementById("pause-btn").setAttribute('hidden','hidden');
var i=event.target.value;

console.log(i);
      var all_data = getjsondata();
      var all_data_bydate = all_data.reduce((r, a) => {
        r[a.startedDate] = [...(r[a.startedDate] || []), a];
        return r;
      }, {});
      // console.log(all_data_bydate);
      var alldates = Object.keys(all_data_bydate);
      var i = parseInt(document.getElementById("range").value);

      // if (i==0) {
       
      // genmap(all_data, window.resultsMap); 
      // }else{
        
      // }
      setmarkersanimate(all_data_bydate[alldates[i]], window.resultsMap);

 });

Array.prototype.getRandom = function (cut) {
  var i = Math.floor(Math.random() * this.length);
  if (cut && i in this) {
    return this.splice(i, 1)[0];
  }
  return this[i];
};


function pause() { 
clearInterval(window.intrvl);

 }