/**
 * Created by JNEP on 11/27/15.
 */
define(['jquery', 'mapbox', 'highstock', 'd3', 'd3_plus', 'arc'], function ($, _, _, d3, _) {

    L.mapbox.accessToken = 'pk.eyJ1Ijoic3JjYyIsImEiOiJlTGVCUUZJIn0.wtVBLySJsD08rO1jtAQNJg';
    var map = L.mapbox.map('map_canvas', 'srcc.b7506415')
        //var map = L.mapbox.map('map_canvas', 'srcc.637a0a6b')
        .setView([41.8369, -87.6847], 8);

    var info = L.control();
    info.onAdd = function (map) {
        this._div = L.DomUtil.create('div', 'info'); // create a div with a class "info"
        this.update();
        return this._div;
    };
    info.update = function () {
        this._div.innerHTML = ( "<i style='color:#fff800' class='fa fa-circle'></i>" + "  Shopping" +
        "<br><i style='color:#ed1b3f' class='fa fa-circle'></i>" + "  Dining" +
        "<br><i style='color:#33ff05' class='fa fa-circle'></i>" + "  Health Care" +
        "<br><i style='color:#009cdd' class='fa fa-circle'></i>" + "Recreation");
    };
    info.addTo(map);

    


    function initialize() {
        $.get('/get_query1', function (dat) {
            var json_p = JSON.parse(dat);
            console.log(json_p);
        });
    }

    return {
        initialize: initialize
    }
});
