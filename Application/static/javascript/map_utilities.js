var response;
var locations;
var polypath;
var polylinePath = new Array();
var markers = new Array();
var bar = document.getElementById('locations-bar');
var barContainer = document.getElementById('barContainer')

function addInfoWindow(marker, location){
    var contentStr = '<div>' + location.timestamp + '</div>' + '<div>' + location.latitude + ',' + location.longitude + '</div>'
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
  var image = initMarkerImage();
  var marker = new google.maps.Marker({
    position: loc,
    map: map,
    title: location.phone_id,
    icon:image
  });
  markers.push(marker);
  polylinePath.push(loc);
  addInfoWindow(marker, location);
}

function addMarkersForLocationsInMap(point_locations,target_map, start_range, end_range){
    for (var i=start_range; i< end_range; i++) {
        addMarker(point_locations[i], target_map);
    }
    updateProgressBar();
}

function updateProgressBar(){
    var w = parseInt(bar.style.width);
    w += 1;
    bar.style.width = w + "%";
    bar.textContent = w + "%";
    if (w > 99) {
        hideProgressBar();
    }
}

function hideProgressBar(){
    barContainer.style.visibility = "hidden";
}

function showProgressBar(){
    barContainer.style.visibility = "visible";
}

function requestLocationsForDeviceID(device_id){
    var request_url = "/json/"+device_id;
    $.get(request_url, function (response){
        locations = response.result;
        console.log('Total locations: '+locations.length)
        showProgressBar();
        createPartitionsForArray(locations, map)
        $.queue.add(partial(drawPolyline, polylinePath, map));
    });
}

function drawPolyline(path,the_map){
    polypath = new google.maps.Polyline({
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

function deletePath(){
    if(polypath){
        polypath.setMap(null);
        polypath = null;
    }
    polylinePath = [];
}

function initMarkerImage(){
    var image = {
        url: "./static/resources/marker.png",
        scaledSize: new google.maps.Size(16,16),
        origin: new google.maps.Point(0,0),
        anchor: new google.maps.Point(8,16)
    };

    return image;
}

function clearAll(){
    deleteMarkers();
    deletePath();
}

function filterResults(deviceID){
    clearAll();
    console.log("Requested filter for deviceID:" + deviceID);
    var start_unix = $('#start_picker').data("DateTimePicker").date().unix();
    var end_unix = $('#end_picker').data("DateTimePicker").date().unix();
    filterDeviceIDWithTime(deviceID,start_unix,end_unix)
}

function filterDeviceIDWithTime(device_id,start_unix,end_unix){
    var request_url = "/json/"+device_id+"/filtered?start="+start_unix+"&end="+end_unix;
    console.log("request url: "+request_url);
    $.get(request_url, function (response){
        locations = response.result;
        console.log('Total locations: '+locations.length)
        showProgressBar();
        createPartitionsForArray(locations, map)
        $.queue.add(partial(drawPolyline, polylinePath, map));
    });
}

