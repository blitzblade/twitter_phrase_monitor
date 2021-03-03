function getcolors() {
  ///colors for charts and map it will be random pick form array
  return [
    "aqua",
    "black",
    "blue",
    "fuchsia",
    "gray",
    "green",
    "lime",
    "maroon",
    "navy",
    "olive",
    "orange",
    "purple",
    "red",
    "silver",
    "teal",
    "white",
    "yellow",
  ];
}

function mapparams(lat, lng, zoom) {
  return {
    center: {
      lat: lat,
      lng: lng,
    },
    zoom: zoom,
    useStaticMap: true,
    backgroundColor: "none",
    zoomControl: true,
  };
}
function getmarkericon() {
  var icon = {
    url: "marker.png", // url
    scaledSize: new google.maps.Size(25, 25), // scaled size
    origin: new google.maps.Point(0, 0), // origin
    anchor: new google.maps.Point(0, 0), // anchor
  };

  return icon;
}

function gettrrorisminterval() {
  return 1000 * 0.7;
}

function getcaliforniainterval() { 
  return 1000*0.05;
 }