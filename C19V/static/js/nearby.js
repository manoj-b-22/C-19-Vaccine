$(document).ready(function() {
    $(".faq-question").on("click", function () {
        if ($(this).parent().hasClass("active")) {
            $(this).next().slideUp();
            $(this).parent().removeClass("active");
        }
        else {
            $(".faq-answer").slideUp();
            $(".faq-singular").removeClass("active");
            $(this).parent().addClass("active");
            $(this).next().slideDown();
        }
    });
});

function initMap() {
    const map = new google.maps.Map(document.getElementById("googleMap"), {
      zoom: 5,
      center: { lat: 28.7041, lng: 77.1025 },
    });
    const geocoder = new google.maps.Geocoder();
    geocodeAddress(geocoder, map);
  }
  function geocodeAddress(geocoder, resultsMap) {
    const address = document.getElementById("address").value;
    geocoder.geocode({ address: address }, (results, status) => {
      if (status === "OK") {
        resultsMap.setCenter(results[0].geometry.location);
        resultsMap.setZoom(8);
        new google.maps.Marker({
          map: resultsMap,
          position: results[0].geometry.location,
          animation: google.maps.Animation.BOUNCE,
        });
      } else {
        alert("Geocode was not successful for the following reason: " + status);
      }
    });
  }

function myMap() {
    var mapProp = {
        center: new google.maps.LatLng(28.7041, 77.1025),
        zoom: 4.2,
    };

    var map = new google.maps.Map(document.getElementById("googleMap"), mapProp);

    var marker = new google.maps.Marker({
        position: new google.maps.LatLng(17.387140, 78.491684),
        animation: google.maps.Animation.BOUNCE
    });
    var infowindow = new google.maps.InfoWindow({
        content: 'Vaccination Centre'
    });

    google.maps.event.addListener(marker, 'click', function () {
        infowindow.open(map, marker);
    });

    marker.setMap(map);

    google.maps.event.addListener(marker, 'click', function () {
        var pos = map.getZoom();
        map.setZoom(10);
        map.setCenter(marker.getPosition(new google.maps.LatLng(17.387140, 78.491684)));
    });

}
