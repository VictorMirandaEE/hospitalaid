(function(L, map_data) {
  function getPoints() {
    return new Promise(function (resolve) {
      resolve(map_data)
    });
  }

  L.Control.SearchBar = L.Control.extend({
    onAdd: function() {
      var input = L.DomUtil.create('input');
      input.className = 'search-bar__input';
      input.placeholder = 'Search hospital';

      var icon = L.DomUtil.create('i');
      icon.className = 'material-icons search-bar__icon';
      icon.innerHTML = 'search';

      var div = L.DomUtil.create('div');
      div.className = 'search-bar';
      div.append(input);
      div.append(icon);

      return div;
    },

    onRemove: function() {}
  });

  L.control.searchBar = function(opts) {
    return new L.Control.SearchBar(opts);
  };

  const map = L
    .map('map', {
      zoomControl: false,
      maxZoom: 16,
    })
    // Pan to Rio de Janeiro
    .setView({ lat: -22.90278, lng: -43.2075 }, 14);

  L
    .tileLayer('https://server.arcgisonline.com/ArcGIS/rest/services/Canvas/World_Light_Gray_Base/MapServer/tile/{z}/{y}/{x}', {
      attribution: 'HospitalAid',
    })
    .addTo(map);

  L.control
    .searchBar({ position: 'topleft' })
    .addTo(map);

  getPoints()
    .then(function (hospitals) {
      hospitals.map(function (hospital) {
        L
          .marker({ lat: hospital.latitude, lng: hospital.longitude })
          .bindPopup(hospital.name + "<br>" + hospital.text + "<a href='" + hospital.link + "'>See</a>")
          .addTo(map);
      })
    });
})(L, map_data);
