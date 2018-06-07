var map_wrapper = 'map_container';
var longitude = 4.7312712;
var latitude = -74.0511726;
var bubble_content =	"<p class='map_contacts'>" +
						"<span>Dirección : </span>" +
						"Cra. 23 No, 148 - 59 Piso 5 Bogotá, Colombia" +
						"</p>";





function initialize() {
	var mapOptions = {
		zoom: 15,
		center: new google.maps.LatLng(longitude, latitude),
		mapTypeId: google.maps.MapTypeId.ROADMAP,
		mapTypeControl: false,
		streetViewControl:false,
		scrollwheel : false,
		zoomControlOptions: {
	      style: google.maps.ZoomControlStyle.SMALL
	    }
	};

	var map = new google.maps.Map(document.getElementById(map_wrapper),mapOptions);

	var marker = new google.maps.Marker({
	  position:  new google.maps.LatLng(longitude, latitude),
	  map: map,
	  icon     : "../static/img/marker3.png"
	});

	var infowindow = new google.maps.InfoWindow({
			content: bubble_content
		});

	google.maps.event.addListener(marker, 'click', function() {
	  infowindow.open(map,marker);
	});
}

google.maps.event.addDomListener(window, 'load', initialize);
