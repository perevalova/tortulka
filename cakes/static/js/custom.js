function initMap() {

    var map = new google.maps.Map(document.getElementById('map'), {
        center: {lat: 50.254991, lng: 28.658287},
        zoom: 15
    });
    var marker = new google.maps.Marker({
        position: center,
    });
}