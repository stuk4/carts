
(function(){
    function centrarMaipu(map){
        map.setCenter({lat:-33.5118659, lng:-70.7719841});
        map.setZoom(13.2);
      }
      var icono = "{% static 'img/50x80.png' %}";
      var icon = new H.map.Icon(icono);
      function addMarkersToMap(map) {
        var maipu = new H.map.Marker({lat:-33.5095529, lng:-70.757001},{icon:icon});
        map.addObject(maipu);
      
      
      }
      
      
      
      
      
      
      
      /**
       * Boilerplate map initialization code starts below:
       */
      
      //Step 1: initialize communication with the platform
      var platform = new H.service.Platform({
        app_id: 'brNJ2r7NYlgWCQ5xQ6LV',
        app_code: '_XCtQXRbZe6Dl9AGPHNyIg',
        useHTTPS: true
      });
      var pixelRatio = window.devicePixelRatio || 1;
      var defaultLayers = platform.createDefaultLayers({
        tileSize: pixelRatio === 1 ? 256 : 512,
        ppi: pixelRatio === 1 ? undefined : 320
      });
      
      //Step 2: initialize a map  - not specificing a location will give a whole world view.
      var map = new H.Map(document.getElementById('map'),
        defaultLayers.normal.map, {pixelRatio: pixelRatio});
      
      //Step 3: make the map interactive
      // MapEvents enables the event system
      // Behavior implements default interactions for pan/zoom (also on mobile touch environments)
      var behavior = new H.mapevents.Behavior(new H.mapevents.MapEvents(map));
      
      // AGREGAR COMPONENTES UI
      var ui = H.ui.UI.createDefault(map, defaultLayers);
      
      //OPCIONES DEL MAPAA
      
      // PRIMERO ES PARA CENTRA EL MAPA EN MAIPUNGA
      centrarMaipu(map);
      // AGREGAR MARCADORES
      addMarkersToMap(map);
})();