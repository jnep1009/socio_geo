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
            "<br><i style='color:#009cdd' class='fa fa-circle'></i>" + "Recreation" +
            "<br><b>Income</b>" +
            "<br><i style='color:#e9bdc6'>-</i>" + "< 20000 USD" +
            "<br><i style='color:#ed80ce'>-</i>" + "20000 - 34999 USD" +
            "<br><i style='color:#c7a7fa'>-</i>" + "35000 - 49999 USD" +
            "<br><i style='color:#bef2bd'>-</i>" + "50000 - 59999 USD" +
            "<br><i style='color:#14c7a9'>-</i>" + "60000 - 75000 USD" +
            "<br><i style='color:#fbc95f'>-</i>" + "75000 - 99999 USD" +
            "<br><i style='color:#fd6137'>-</i>" + "> 100000 USD"
        );
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
