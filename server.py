import tornado.httpserver
import tornado.ioloop
import tornado.web
import psycopg2 as DB
import os
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
        self.write('hi')



settings = {
    # go to the file and go find "www"
    "static_path": os.path.join(os.path.dirname(__file__), "static"),
    "xsrf_cookies": True,
}

handlers = [
    (r"/", MainHandler),
    (r"/get_query1", get_query1)
]

application = tornado.web.Application(handlers, **settings)

if __name__ == "__main__":
    application.listen(8500)
    tornado.ioloop.IOLoop.current().start()
