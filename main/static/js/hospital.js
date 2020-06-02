/* 
  REFERENCES:
  https://derickrethans.nl/leaflet-and-nominatim.html
  https://github.com/joindin
*/

var map;
var marker;
var addrSelector = $('#addr_selection');

function load_map() {
  var lat = map_latitude;
  var lon = map_longitude;
  var zoomLevel = 19;
  var location;

  if (map) {
    map.remove();
  }

  map = new L.Map('id_map_account', { zoomControl: true });

  // add the OpenStreetMap tiles
  var osmUrl = 'http://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',
      osmAttribution = '&copy; <a href="https://openstreetmap.org/copyright">OpenStreetMap contributors</a>',
      osm = new L.TileLayer(osmUrl, { maxZoom: zoomLevel, attribution: osmAttribution });

  map.setView(new L.LatLng(lat, lon), zoomLevel).addLayer(osm);

  location = new L.LatLng(lat, lon);
  marker = L.marker(location, { draggable: true }).addTo(map);
  marker.on('dragend', function () { location = marker.getLatLng(); placeMarker(location) });
}

function placeMarker(location) {
  if (!marker) {
    marker = L.marker(location, { draggable: true }).addTo(map);
    marker.on('dragend', function () { location = marker.getLatLng(); placeMarker(location) });
  } else {
    marker.setLatLng(location);
  }

  console.log("location.lat1="+location.lat);
  console.log("location.lng1="+location.lng);

  $('#id_hospital_latitude').val(location.lat);
  $('#id_hospital_longitude').val(location.lng);
  //$('#id_hospital_country').val("Country");
}

function chooseAddr(lat, lng) {
  var location = new L.LatLng(lat, lng);

  addrSelector.hide();
  map.panTo(location);
  placeMarker(location);
}

function addrSearch(type) {
  var hospitalName        = document.getElementById("id_hospital_name");
  var hospitalAddress     = document.getElementById("id_hospital_address");
  var hospitalCity        = document.getElementById("id_hospital_city");
  var hospitalPostCode    = document.getElementById("id_hospital_postcode");
  var hospitalCountry     = document.getElementById("id_hospital_country");
  var hospitalFullAddress = hospitalAddress.value + ", " +
                            hospitalCity.value + ", " +
                            hospitalPostCode.value + ", " +
                            hospitalCountry.value;

  if(type == 'address') {
    searchText = hospitalFullAddress;   
  } else {
    searchText = hospitalName.value;
  }

  console.log("searchText = "+searchText);

  $.getJSON('https://nominatim.openstreetmap.org/search?format=json&limit=5&q=' + searchText, function(data) {
    var items = [];

    $.each(data, function (key, val) {
      console.log("display_name="+val.display_name);
      console.log("lat="+val.lat);
      console.log("lon="+val.lon);
      items.push("<li><a href='#' onclick='chooseAddr(" + val.lat + ", " + val.lon + ");return false;'>" + val.display_name + '</a></li>');
    });

    addrSelector.show(100);

    if (items.length != 0) {
      addrSelector.empty();
      $('<ul/>', {
        'class': 'my-new-list',
        html: items.join('')
      }).appendTo(addrSelector);
    } else {
      addrSelector.empty();
      $('<p>', { html: "No results found" }).appendTo(addrSelector);
    }
  });
}

$(document).ready(function () {
  load_map();

  // prevent submitting the form on <ENTER>.
  $(window).keydown(function (event) {
    if (event.keyCode == 13) {
      event.preventDefault();
      return false;
    }
  });

  // <ESC> closes results list.
  $(window).keyup(function (event) {
    if (event.keyCode == 27) {
      event.preventDefault();
      addrSelector.hide();
      return false;
    }
  });
});
