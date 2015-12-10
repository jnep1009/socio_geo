import tornado.httpserver
import tornado.ioloop
import tornado.web
import psycopg2 as DB
import math
import numpy as np
import traceback
import os
import collections
import pandas as pd
from scipy.spatial import distance
from geopy.distance import vincenty
import requests
import json


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("index.html")


class getType():
    """Get Types of transportations and income."""

    def query_trans(self, q_num):
        """
        Query a mode of transportation.
        :param q_num: the number of transportation mode.
        :return:
        """
        trans_m = {1: 'walking', 2: 'bicycling', 3: 'driving', 4: 'driving',
                   5: 'transit', 6: 'transit', 7: 'transit', 8: 'transit', 9: 'driving',
                   10: 'driving', 11: 'driving', 12: 'driving', 14: 'transit', 15: 'transit'}
        return trans_m[q_num]

    def query_income(self, q_in):
        """
        Query a mode of transportation.
        :param q_num: the number of income categories.
        :return:
        """
        title_i = {1: '<15000', 2: '20000-34999', 3: '35000-49999', 4: '50000-59999',
                   5: '60000-74999', 6: '75000-99999', 7: '>100000'}
        return title_i[q_in]


class get_query1(tornado.web.RequestHandler):
    def get(self):
        '''Start processes '''
        self.data = []
        self.allDist = []
        chicago_cbd = (41.8369, -87.6847)
        conn = DB.connect('dbname=project_urban user=june')
        cur = conn.cursor()
        q_str = '''select avg(actv_length), income from person, trip, household
                    where person.pp_id = trip.pp_id and household.hh_id = person.hh_id
                    and trip.date ='1' and trip.trip_purpose ='3' and income <> '9' and
                    exists( select hh_id from person group by hh_id having count(pp_id) > 3)
                    group by income; ''';
        cur.execute(q_str)
        rows = cur.fetchall()
        for row in rows:
            self.data.append({
                'name': getType().query_income(int(row[1])),
                'data': "%.2f" % round(float(row[0]), 2)
            })
        self.write(json.dumps(self.data))


class get_query2(tornado.web.RequestHandler):
    def get(self):
        '''Start processes '''
        self.data = []
        self.allDist = []
        conn = DB.connect('dbname=project_urban user=june')
        cur = conn.cursor()
        q_str = ''' select trip_des.description, avg(case when trip.date in ('1','2','3','4','5') then actv_length end) as weekday,
                    avg(case when trip.date in ('6','7') then actv_length end) as weekend from trip, trip_des where trip_des.trip_purpose = trip.trip_purpose
                    and trip.trip_purpose in ('2','3','5','13','15','17','18','19','20','21') group by description; ''';
        cur.execute(q_str)
        rows = cur.fetchall()
        for row in rows:
            self.data.append({
                'name': row[0],
                'data': ["%.2f" % round(float(row[1]), 2), "%.2f" % round(float(row[2]), 2)]
            })
        print(self.data)
        self.write(json.dumps(self.data))


class get_query4(tornado.web.RequestHandler):
    def get(self):
        '''Start processes '''
        self.data = []
        self.allDist = []
        conn = DB.connect('dbname=project_urban user=june')
        cur = conn.cursor()
        q_str = ''' select b.x_lng,b.y_lat, b.pre_x, b.pre_y from (
                    select trip.pp_id, trip.trip_no, trip.day, place.x_lng,place.y_lat,
                    lag(place.x_lng) over client_window as pre_x,
                    lag(place.y_lat) over client_window as pre_y,
                    trip.trip_length
                    from place_loc as place, trip
                    where trip.place_id = place.place_id
                    and cast(trip.trip_no as integer) <= 3
                    window client_window as (partition by trip.pp_id, day order by trip.trip_no)
                    order by trip.pp_id) as b where b.trip_no <> '1'
                    and b.pre_x is not null and b.x_lng <> b.pre_x and b.x_lng is not null limit 5000;''';
        cur.execute(q_str)
        rows = cur.fetchall()
        for row in rows:
            self.data.append([[row[3], row[2]], [row[1], row[0]]])
        self.write(json.dumps(self.data))


settings = {
    # go to the file and go find "www"
    "static_path": os.path.join(os.path.dirname(__file__), "static"),
    "xsrf_cookies": True,
}

handlers = [
    (r"/", MainHandler),
    (r"/get_query1", get_query1),
    (r"/get_query2", get_query2),
    (r"/get_query4", get_query4)
]

application = tornado.web.Application(handlers, **settings)

if __name__ == "__main__":
    application.listen(8500)
    tornado.ioloop.IOLoop.current().start()
