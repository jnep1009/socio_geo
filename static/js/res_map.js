/**
 * Created by JNEP on 11/27/15.
 */
define(['jquery', 'mapbox', 'highstock', 'd3', 'd3_plus', 'arc'], function ($, _, _, d3, _) {

    L.mapbox.accessToken = 'pk.eyJ1Ijoic3JjYyIsImEiOiJlTGVCUUZJIn0.wtVBLySJsD08rO1jtAQNJg';
    var map = L.mapbox.map('map_canvas', 'srcc.0df35dc0')
        //var map = L.mapbox.map('map_canvas', 'srcc.637a0a6b')
        .setView([41.8369, -87.6847], 8);

    var info = L.control();
    info.onAdd = function (map) {
        this._div = L.DomUtil.create('div', 'info'); // create a div with a class "info"
        this.update();
        return this._div;
    };
    info.update = function () {
        this._div.innerHTML = ( "<i style='color:#1c1e24' class='fa fa-circle'></i>" + "  Manufactuting" +
        "<br><i style='color:#1b55ed' class='fa fa-circle'></i>" + "  Transportation" +
        "<br><i style='color:#6765bd' class='fa fa-circle'></i>" + "  Communications" +
        "<br><i style='color:#a8afdf' class='fa fa-circle'></i>" + "  Retail" +
        "<br><i style='color:#ebc732' class='fa fa-circle'></i>" + "  Service" +
        "<br><i style='color:#c07c53' class='fa fa-circle'></i>" + "  Government" +
        "<br><i style='color:#eb2b10' class='fa fa-circle'></i>" + "  Others");
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
