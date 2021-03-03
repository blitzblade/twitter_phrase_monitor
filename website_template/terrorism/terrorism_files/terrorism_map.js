// Create the script tag, set the appropriate attributes
var script = document.createElement("script");
script.src =
  "https://maps.googleapis.com/maps/api/js?key=AIzaSyAgDf2DBQwy33XYxD7jKmO0AIo5TT06Q0U&callback=initMap";
script.defer = true;
let resultsMap = null;
let geocoder = null;
let markers = [];
// Attach your callback function to the `window` object
window.initMap = function () {
  // JS API is loaded and available
 geocoder = new google.maps.Geocoder();
//   alert("works");
resultsMap = new google.maps.Map(
  document.getElementById("map"),
  mapparams(51.4934, 0.0098,2)
);
getAjaxdata(resultsMap, geocoder);
};

// Append the 'script' element to 'head'
document.head.appendChild(script);

function geocodeAddress(geocoder, resultsMap,address) {
    // console.log(geocoder);
//   const address = document.getElementById("address").value;
var marker=null;
  geocoder.geocode({ address: address.location }, (results, status) => {
    if (status === "OK") {
      // resultsMap.setCenter(results[0].geometry.location);
      console.log(results);
      addMarker(results[0].geometry.location, resultsMap,address);
    // marker = new google.maps.Marker({
    //   animation: google.maps.Animation.DROP,

    //   map: resultsMap,
    //   position: results[0].geometry.location,
    // });
    } else if(status === google.maps.GeocoderStatus.OVER_QUERY_LIMIT){

setTimeout(() => {
  geocodeAddress(geocoder, resultsMap,address);
}, 200);

    }
    
    else {
      alert("Geocode was not successful for the following reason: " + status);
    }
  });
}
function getAjaxdata(resultsMap, geocoder) {
  var data = null;

  var xhr = new XMLHttpRequest();
  xhr.withCredentials = false;

  xhr.addEventListener("readystatechange", function () {
    if (this.readyState === this.DONE) {
      var res = JSON.parse(this.responseText);
      var year = moment().format('YYYY');
      document.getElementById("mapyear").innerHTML=year;
      var all_data = getalldata_terrorism(res);
      window.markers = getmarkers(
        geocoder,
        resultsMap,
        all_data,
        year
      );
      console.log(window.markers);
    }
  });

  xhr.open("GET", "http://45.63.15.162:8000/data/terrorist_incidents.json");

  xhr.send(data);
}


function getmarkers(geocoder, resultsMap, data, year) {
  var gorupdeyear = data.reduce((r, a) => {
    r[a.year] = [...(r[a.year] || []), a];
    return r;
  }, {});

  var markers = [];
console.log();
var i=0;
var apn = "";
var i = 0;
  gorupdeyear[year].forEach((element) => {
  // gorupdeyear[year].forEach((element) => {
    // if (1==1) {
      markers.push(addMarker(element.cords, resultsMap, ""));
      // markers.push();
  
// }
++i;
    apn += "<tr>";
    apn += "<td>" + i + "</td>";
    apn += "<td>" + element.cords + "</td>";
    apn += "</tr>";

  });
  // console.log(markers);
      // document.getElementById("table").innerHTML = apn;
      return markers;
}


 function addMarker(location, map,label) {
   // Add the marker at the clicked location, and add the next-available label
   // from the array of alphabetical characters.
   var color=getcolors().sample();
   var icn= {
       path: google.maps.SymbolPath.CIRCLE,
       scale: 10,
       fillColor: color,
       fillOpacity: 1,
       strokeWeight: 0.6,
       strokeColor: getcolors().sample(),
     };
    
   var marker = new google.maps.Marker({
     position: location,
     //  label: label.location,

     map: map,
    //  animation: google.maps.Animation.DROP,
     icon: getmarkericon(),
   });
   return marker;
 }


 function mapanimate() {

  var data = null;

  var xhr = new XMLHttpRequest();
  xhr.withCredentials = false;

  xhr.addEventListener("readystatechange", function () {
    if (this.readyState === this.DONE) {

      var res = JSON.parse(this.responseText);
      var year = moment().format("YYYY");
      var all_data = getalldata_terrorism(res);
      setMapOnAll(null);
       
var gorupdeyear = all_data.reduce((r, a) => {
  r[a.year] = [...(r[a.year] || []), a];
  return r;
}, {});


      
      var minyear=1970;
       interval = setInterval(() => {
         setMapOnAll(null);
         if (gorupdeyear[minyear] === undefined) {
         } else {
           if (minyear == year) {
             clearInterval(interval);
             window.markers = getmarkers(
               geocoder,
               resultsMap,
               all_data,
               minyear
             );
           } else {
             window.markers = getmarkers(
               geocoder,
               resultsMap,
               all_data,
               minyear
             );
           }
         }
         document.getElementById("mapyear").innerHTML = minyear;
         document.getElementById("range").value = minyear;

         // alert(minyear);
         ++minyear;
       }, gettrrorisminterval());
   
    }
  });

  xhr.open("GET", "http://45.63.15.162:8000/data/terrorist_incidents.json");

  xhr.send(data);
  
 }
 function setMapOnAll() {
   for (let i = 0; i < window.markers.length; i++) {
     window.markers[i].setMap(null);
   }
 }
