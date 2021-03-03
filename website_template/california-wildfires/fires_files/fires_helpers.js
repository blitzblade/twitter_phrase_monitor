
// Append the 'script' element to 'head'
// document.head.appendChild(script);


   Array.prototype.diff = function (a) {
     return this.filter(function (i) {
       return a.indexOf(i) < 0;
     });
   };

   Array.prototype.sum = function (prop) {
     var total = 0;
     for (var i = 0, _len = this.length; i < _len; i++) {
       total += this[i][prop];
     }
     return total;
   };


           function filterdate(startDate, endDate, data) {
             var filteredData = data.filter((a) => {
               var date = new Date(a.startedDate);
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
function renderChart(data_set, labels = [], myChart_data) {
  myChart_data.data.datasets = data_set;
  myChart_data.data.labels = labels;
  myChart_data.update();
}

function get_alldata(data) {
  var set = [];
  data.forEach((element) => {
    element.year = moment(element.startedDate).format("YYYY");

    if (element.acres == "NAN" || element.acres == "") {
      element.acres = 0;
    } else {
      element.acres = parseFloat(numeral(element.acres).value());
    }
    element.month_in_number = moment(element.startedDate).format("MM");
    element.month_in_name = moment(element.startedDate).format("MMMM");
    set.push(element);
  });
  return set;
}


function getjsondata() { 
var value=[];
var json_val = document.getElementById("json_val").value;

if (json_val!="") {

  value = JSON.parse(json_val);
}

return value;

 }