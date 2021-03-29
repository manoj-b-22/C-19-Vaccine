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

function myMap() {
    var mapProp = {
        center: new google.maps.LatLng(17.387140, 78.491684),
        zoom: 5,
    };

    var map = new google.maps.Map(document.getElementById("googleMap"), mapProp);

    var marker = new google.maps.Marker({
        position: new google.maps.LatLng(17.387140, 78.491684),
        animation: google.maps.Animation.BOUNCE
    });
    var infowindow = new google.maps.InfoWindow({
        content: "Shwetha-Hospitals"
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
