(function(){
    var txtlat = document.getElementById('txtlatitud');
    var txtlon = document.getElementById('txtlongitud');
    if (navigator.geolocation) {
        //       const watcher = navigator.geolocation.watchPosition(mostrarUbicacion);
        
        // setTimeout(() => {
        //   navigator.geolocation.clearWatch(watcher);
        // }, 5000);
        
           navigator.geolocation.getCurrentPosition(mostrarUbicacion);
        }
        
          
        function mostrarUbicacion (ubicacion) {
          const lng = ubicacion.coords.longitude;
          const lat = ubicacion.coords.latitude;
            txtlat.value = lat;
            txtlon.value = lng;
          console.log(`longitud: ${ lng } | latitud: ${ lat }`);
        }

        


})();

