(function(L, axios) {
  function getPoints() {
    // Mock real api with fake data for now
    // fixme Use `axios` for fetching data from real API
    return new Promise(function (resolve) {
      resolve([
        {
          name: 'hospital name',
          town: 'Rio de janeiro',
          country: 'Brasil',
          latitude: -22.901,
          longitude: -43.206,
          n_aidrequests: 23,
        },
        {
          name: 'another hospital',
          town: 'Rio de janeiro',
          country: 'Brasil',
          latitude: -22.903,
          longitude: -43.208,
          n_aidrequests: 24,
        },
      ])
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
          .bindPopup(hospital.name)
          .addTo(map);
      })
    });
})(L, axios);
