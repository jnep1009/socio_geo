/**
 * Created by june on 10/2/15.
 */

requirejs.config({
    'baseUrl': '/static/js',
    'paths': {
        'jquery': 'https://ajax.googleapis.com/ajax/libs/jquery/2.1.3/jquery.min',
        'bootstrap': 'http://maxcdn.bootstrapcdn.com/bootstrap/3.3.2/js/bootstrap.min',
        'mapbox': 'https://api.tiles.mapbox.com/mapbox.js/v2.2.1/mapbox',
        'highstock': 'http://code.highcharts.com/stock/highstock',
        'd3': 'https://cdnjs.cloudflare.com/ajax/libs/d3/3.5.9/d3',
        'c3': 'https://cdnjs.cloudflare.com/ajax/libs/c3/0.4.10/c3.min',
        'date_js': 'https://cdnjs.cloudflare.com/ajax/libs/datejs/1.0/date.min',
        'd3_plus': 'https://cdnjs.cloudflare.com/ajax/libs/d3plus/1.8.0/d3plus',
        'arc': 'https://api.mapbox.com/mapbox.js/plugins/arc.js/v0.1.0/arc'
    },
    /**
     * Declare the dependencies.
     */
    'shim': {
        'bootstrap': {
            deps: ['jquery']
        },
        'res_map': {
            deps: ['jquery','mapbox','highstock','d3','date_js','d3_plus','arc']
        }
    }
});

/**
 * start running everytime everything begins to run this will run first
 */
require(['jquery','mapbox'], function ($) {
    require(['res_map'], function (main_js) {
        main_js.initialize();
    });
});
