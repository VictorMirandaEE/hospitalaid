(function(L, map_data) {
  function getPoints() {
    return new Promise(function (resolve) {
      resolve(map_data)
    });
  }

  function createPopup(hospital) {
    var temp = document.getElementById("map-popup").content.cloneNode(true);
    hosp = temp.getElementById("hospitalname");
    hosp.textContent = hospital.name;
    link = temp.getElementById("hospitallink");
    link.href = hospital.link;
    r = temp.getElementById("repair");
    r.textContent = 2;
    s = temp.getElementById("supply");
    s.textContent = 1;
    return temp;
  }

  const map = L
    .map('map', {
      zoomControl: false,
      maxZoom: 16,
    })
    // Pan to Rio de Janeiro
    .setView({ lat: -3.22278, lng: -0.2075 }, 6);

  L
    .tileLayer('https://server.arcgisonline.com/ArcGIS/rest/services/Canvas/World_Light_Gray_Base/MapServer/tile/{z}/{y}/{x}', {
      attribution: 'HospitalAid',
    })
    .addTo(map);

  getPoints()
    .then(function (hospitals) {
      hospitals.map(function (hospital) {
        L
          .marker({ lat: hospital.latitude, lng: hospital.longitude })
          .bindPopup(createPopup(hospital), {closeButton: false})
          .addTo(map);
      })
    });
})(L, map_data);
