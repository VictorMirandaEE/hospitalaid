(function(L, map_data) {
  function getPoints() {
    return new Promise(function (resolve) {
      resolve(map_data)
    });
  }

  function createPopup(hospital) {
    var map_popup = document.getElementById("id_map-popup").content.cloneNode(true);

    hosp = map_popup.getElementById("id_hospital-name");
    hosp.textContent = hospital.name;

    link = map_popup.getElementById("id_hospital-link");
    link.href = hospital.link;

    supply = map_popup.getElementById("id_supply");
    supply.textContent = hospital.supply_count;

    repair = map_popup.getElementById("id_repair");
    repair.textContent = hospital.repair_count;

    return map_popup;
  }

  // initialize Leaflet
  var map = L.map('id_map').fitWorld();

  map.locate({setView: true, maxZoom: 16});

  function onLocationFound(e) {
    var radius = e.accuracy;

    L.marker(e.latlng).addTo(map)
        .bindPopup("You are within " + radius + " meters from this point").openPopup();

    L.circle(e.latlng, radius).addTo(map);
  }

  map.on('locationfound', onLocationFound);

  function onLocationError(e) {
    alert(e.message);
  }

  map.on('locationerror', onLocationError);

  // add the OpenStreetMap tiles
  L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    maxZoom: 19,
    attribution: '&copy; <a href="https://openstreetmap.org/copyright">OpenStreetMap contributors</a>'
  }).addTo(map);

  // show the scale bar on the lower left corner
  L.control.scale().addTo(map);

  L.easyButton('<img class="h-5 inline" src="/static/images/hospital-pin-black.svg">', function(btn, map){
    fitBounds();
  }, 'Zoom all').addTo(map);

//  L.easyButton('<span class="font-bold text-lg align-middle">&ofcir;</span>', function(btn, map){
//    fitBounds();
//  }, 'Show your location').addTo(map);


  var hospitalIcon = L.icon({
      iconUrl: '/static/images/hospital-pin-black.svg',

      iconSize:     [32, 39], // size of the icon
      iconAnchor:   [16, 39], // point of the icon which will correspond to marker's location
      popupAnchor:  [0, -42]  // point from which the popup should open relative to the iconAnchor
  });

  var hospitalBlueIcon = L.icon({
      iconUrl: '/static/images/hospital-pin-blue.png',

      iconSize:     [32, 39], // size of the icon
      iconAnchor:   [16, 39], // point of the icon which will correspond to marker's location
      popupAnchor:  [0, -42]  // point from which the popup should open relative to the iconAnchor
  });

  var hospitals_group = L.featureGroup().addTo(map);

  function fitBounds () {
    map.fitBounds(hospitals_group.getBounds());
  }

  // fit hospitals_group after 1 second.
  setTimeout(function () {
    //fitBounds();
  }, 1);

  // add markers to the hospitals_group
  getPoints()
    .then(function (hospitals) {
      hospitals.map(function (hospital) {
        L
          .marker({ lat: hospital.latitude, lng: hospital.longitude },
          {icon: hospitalIcon})
          //.on('click', function(e) { e.target.setIcon(hospitalBlueIcon); })
          .on('click', function() {
            this.bindPopup(createPopup(hospital), {closeButton: false});
          })
          .addTo(hospitals_group);
      })
    });
})(L, map_data);
