(function(L, map_data) {
  function getPoints() {
    return new Promise(function (resolve) {
      resolve(map_data)
    });
  }

  function createPopup(hospital) {
    var mapPopup = document.getElementById("id_map_popup").content.cloneNode(true);

    hosp = mapPopup.getElementById("id_hospital_name");
    hosp.textContent = hospital.name;

    link = mapPopup.getElementById("id_hospital_link");
    link.href = hospital.link;

    supply = mapPopup.getElementById("id_supply");
    supply.textContent = hospital.supply_count;

    repair = mapPopup.getElementById("id_repair");
    repair.textContent = hospital.repair_count;

    return mapPopup;
  }

  // initialize Leaflet
  var map = L.map('id_map').fitWorld();

  var myMarker;

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

  var hospitalGroup = L.featureGroup().addTo(map);
  var hospitalArray = new Array();
  var nearestGroup  = L.featureGroup().addTo(map);

  map.locate({setView: true, maxZoom: 19});

  function onLocationFound(e) {
    if(!myMarker) {
      myMarker = L.marker(e.latlng).addTo(map);
    }
    findNearestMarker();
  }

  map.on('locationfound', onLocationFound);

  function onLocationError(e) {
    alert(e.message);
    fitBounds();
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

  function locate() {
    if (!navigator.geolocation){
      alert("<p>Sorry, your browser does not support Geolocation</p>");
      return;
    }

    map.locate({setView: true, maxZoom: 19});
    findNearestMarker();
  };

  L.easyButton('<span class="font-bold text-lg align-middle">&ofcir;</span>', function(btn, map){
    findNearestMarker();
  }, 'Find your location').addTo(map);

  function fitBounds () {
    map.fitBounds(hospitalGroup.getBounds());
  }

  // add markers to the hospitalGroup
  getPoints()
    .then(function (hospitals) {
      hospitals.map(function (hospital) {
        var marker =
        L
          .marker({ lat: hospital.latitude, lng: hospital.longitude },
          {icon: hospitalIcon})
          //.on('click', function(e) { e.target.setIcon(hospitalBlueIcon); })
          .on('click', function() {
            this.bindPopup(createPopup(hospital), {closeButton: false});
          })
          .addTo(hospitalGroup);
        hospitalArray.push(marker);
      })
    });

  function findNearestMarker() {
    var minDist;
    var nearestMarker;
    var hospitalLatLng;
    var myLatLng;
    var distance;

    if (hospitalArray.length != 0) {
      myLatLng = myMarker.getLatLng();
      hospitalLatLng = hospitalArray[0].getLatLng();
      minDist = hospitalLatLng.distanceTo(myLatLng);
      nearestMarker = hospitalArray[0];

      for(ii=0 ; ii < hospitalArray.length ; ii++) {
        hospitalLatLng = hospitalArray[ii].getLatLng();
        distance = hospitalLatLng.distanceTo(myLatLng);

        if (distance < minDist) {
          minDist = distance;
          nearestMarker = hospitalArray[ii];
        }
      }

      myMarker.addTo(nearestGroup);
      nearestMarker.addTo(nearestGroup);
      map.flyToBounds(nearestGroup.getBounds());
    } else {
      fitBounds();
    }
  }

})(L, map_data);
