function buildmap(state) {  
  console.log(`building map for ${state}`);
  queryUrl = `https://api.weather.gov/alerts/active?status=actual&message_type=alert&area=${state}&severity=Severe`;


var map = L.map('map').setView([44.96, -103.77], 5);

L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
}).addTo(map);

d3.json(queryUrl).then(function(data){
  let coords = data.features[0].geometry;
  // console.log(coords);
  L.polygon(coords,{
    color: "purple",
    fillColor: "purple",
    fillOpacity: 0.75
  }).addTo(map);
})};

// d3.select('#buildmap').on('click',buildmap(d3.select('#stateselector').value)); 
// console.log(d3.select('#stateselector').options[d3.select('#stateselector')[selectedIndex].value);

function init() {
  console.log('app initialized')
  var selector = d3.select("#stateselector");

  d3.json('/states').then(function(data){
    // console.log("You have data");
    // console.log(data);
    data.forEach(state => {
      selector
      .append('option')
      .property('value',state)
      .text(state);
    });
  })
  buildmap("AL");

}
init();