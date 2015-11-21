var response;
var locations;
var polylinePath = new Array();
var markers = new Array();

function addInfoWindow(marker, contentStr){
    var infoWindow = new google.maps.InfoWindow({
        content: contentStr
    });
    marker.addListener('click', function(){
        infoWindow.open(map,marker);
    });
}

// Adds a marker to the map.
function addMarker(location, map) {
  var loc = {lat: location.latitude, lng: location.longitude};
  var marker = new google.maps.Marker({
    position: loc,
    map: map,
    title: location.phone_id
  });
  markers.push(marker);
  polylinePath.push(loc);
  var contentStr = '<div>' + new Date(location.timestamp) + '</div>' + '<div>' + location.latitude + ',' + location.longitude + '</div>'
  addInfoWindow(marker, contentStr);
}

function addMarkersForLocationsInMap(point_locations,target_map){
    for (var i=0; i< point_locations.length; i++){
        addMarker(point_locations[i], target_map);
    }
}

function requestLocationsForDeviceID(device_id){
    var request_url = "/json/"+device_id;
    $.get(request_url, function (r){
        response = r;
        locations = response.result;
        addMarkersForLocationsInMap(locations,map);
        drawPolyline(polylinePath,map)
    });
}

function drawPolyline(path,the_map){
    var polypath = new google.maps.Polyline({
        path: path,
        geodesic: true,
        strokeColor: '#0000FF',
        strokeOpacity: 0.8,
        strokeWeight: 2
    });
    polypath.setMap(the_map);
}

function hideMarkers(){
    setMapOnMarkers(null);
}

function showMarkers(the_map){
    setMapOnMarkers(the_map);
}

function setMapOnMarkers(map){
    for (var i=0; i < markers.length; i++){
        markers[i].setMap(map);
    }
}

function deleteMarkers(){
    hideMarkers();
    markers = [];
}