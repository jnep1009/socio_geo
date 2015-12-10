import psycopg2 as DB
import requests
import time
import datetime

class getType():
    """Get Types of transportations and income."""
    def query_trans(self, q_num):
        """
        Query a mode of transportation.
        :param q_num: the number of transportation mode.
        :return:
        """
        trans_m = {  1:'walking', 2:'bicycling',3:'driving',4:'driving',
             5:'transit', 6:'transit',7:'transit', 8:'transit', 9:'driving',
             10:'driving',11:'driving',12:'driving',14:'transit', 15:'transit'}
        return trans_m[q_num]

    def travel_time(self, trans_mode, origin, des):
        """
        Get the travel distance based on a mode of transportation.
        :param mode of transportation, [h_lat, h_lng], [des_lat[y], des_lng[x]]:
        :return [distance ,travel time]:
        """
        based_url = 'https://maps.googleapis.com/maps/api/distancematrix/json'
        params = "origins=%.7f,%.7f&destinations=%.7f,%.7f&mode=%s" %(origin[0], origin[1], des[0], des[1], trans_mode)
        url = based_url + "?" + params + "&key=" + "AIzaSyBNoTJMDEHQTo_8RoBvlP0PV-RmJbf6smU"
        res = requests.get(url)
        res_json = res.json()
        if res_json['rows'][0]['elements'][0]['status'] == 'OK':
            time_t = res_json['rows'][0]['elements'][0]['duration']['text']
            trip_distance = res_json['rows'][0]['elements'][0]['distance']['text']
            print(time_t, trip_distance)
            if "hour" not in time_t:
                travel_time = time.strptime(time_t.split(' ')[0], '%M')
                travel_time = datetime.timedelta(minutes=travel_time.tm_min).total_seconds()/60
                if int(travel_time) < 5:
                    travel_time = 2
                else:
                    travel_time = round((travel_time/5))*5
            else:
                travel_time_hm = "%s,%s" %(time_t.split(' ')[0],time_t.split(' ')[2])
                travel_time = time.strptime(travel_time_hm,'%H,%M')
                travel_time = round((datetime.timedelta(hours=travel_time.tm_hour,minutes=travel_time.tm_min).total_seconds()/60)/5)*5
            if "km" not in trip_distance:
                trip_distance = trip_distance.split(' m')[0]
            else:
                trip_distance = float(trip_distance.split(' km')[0]) * 1000
            return [travel_time, trip_distance]
        else:
            return 0


connString = 'dbname=urban_proj user=june'
conn = DB.connect(connString)
cur = conn.cursor()

''' Get Travel Distance, Time by income'''
for race in [1,2,3,4,7]:
    for i_trip in [13,17,18,20]:
        q_str = ''' select race, trip.trans_mode, person.hh_id, person.p_id,
                    (select x_lng from place_loc where place_loc.place_id = household.hh_loc) as house_lng,
                    (select y_lat from place_loc where place_loc.place_id = household.hh_loc) as house_lat,
                    place_loc, trip.day, trip.trip_no,
                    (select x_lng from place_loc where place_loc.place_id = trip.place_loc) as trip_lng,
                    (select y_lat from place_loc where place_loc.place_id = trip.place_loc) as trip_lng
                    from person,trip,household
                    where person.hh_id = trip.hh_id
                    and person.p_id = trip.p_id
                    and household.hh_id = person.hh_id
                    and trip.trans_mode not in ('97','98','99')
                    and race='%s' and trip_purpose='%s' ;''' %(race, i_trip)
        cur.execute(q_str)
        rows = cur.fetchall()
        for row in rows:
            print(row)
            data = []
            allDist = []
            if row[4] is not None and row[9] is not None:
                race = row[0]
                trans_mode = getType().query_trans(int(row[1]))
                hh_latlng = (row[5],row[4])
                trip_latlng = (row[10],row[9])
                ''' Composit Primary Key from hh_id,p_id,trip_day,trip_no'''
                unique_id = row[2] + "_" + row[3] +"_"+ row[7] +"_"+ row[8]
        #       Get travel distanct + time based on xy and mode of transportation
        #       Result = [distance, time]
                getTimeDist = getType().travel_time(trans_mode,hh_latlng,trip_latlng)
                if getTimeDist != 0:
                    travel_time = getTimeDist[0]
                    travel_distance = getTimeDist[1]
                    try:
                        cur.execute(
                            "INSERT INTO result_ethic (race, travel_time, distance, trip_purpose, trans_mode, trip_no) VALUES (%s,%s,%s,%s,%s,%s)",
                            (race, travel_time, travel_distance, i_trip, trans_mode, unique_id ))
                        conn.commit()

                    except DB.IntegrityError as e:
                        cur.close()
                        conn.close()
                        conn = DB.connect(connString)
                        cur = conn.cursor()
                        print


''' Get Travel Distance, Time by income'''

for income in [1,2,3,4,5,6]:
    for i_trip in [13,17,18,20]:
        q_str = ''' select income, trip.trans_mode, person.hh_id, person.p_id,
                    (select x_lng from place_loc where place_loc.place_id = household.hh_loc) as house_lng,
                    (select y_lat from place_loc where place_loc.place_id = household.hh_loc) as house_lat,
                    place_loc, trip.day, trip.trip_no,
                    (select x_lng from place_loc where place_loc.place_id = trip.place_loc) as trip_lng,
                    (select y_lat from place_loc where place_loc.place_id = trip.place_loc) as trip_lng
                    from person,trip,household
                    where person.hh_id = trip.hh_id
                    and person.p_id = trip.p_id
                    and household.hh_id = person.hh_id
                    and trip.trans_mode not in ('97','98','99')
                    and race = '1'
                    and income='%s' and trip_purpose='%s'; ''' %(income, i_trip)
        cur.execute(q_str)
        rows = cur.fetchall()
        for row in rows:
            print(row)
            data = []
            allDist = []
            if row[4] is not None and row[9] is not None:
                income = row[0]
                trans_mode = getType().query_trans(int(row[1]))
                hh_latlng = (row[5],row[4])
                trip_latlng = (row[10],row[9])
                ''' Composit Primary Key from hh_id,p_id,trip_day,trip_no'''
                unique_id = row[2] + "_" + row[3] +"_"+ row[7] +"_"+ row[8]
        #       Get travel distanct + time based on xy and mode of transportation
        #       Result = [distance, time]
                getTimeDist = getType().travel_time(trans_mode,hh_latlng,trip_latlng)
                if getTimeDist != 0:
                    travel_time = getTimeDist[0]
                    travel_distance = getTimeDist[1]
                    try:
                        cur.execute(
                            "INSERT INTO result_income (income, travel_time, distance, trip_purpose, trans_mode, trip_no) VALUES (%s,%s,%s,%s,%s,%s)",
                            (income, travel_time, travel_distance, i_trip, trans_mode, unique_id ))
                        conn.commit()

                    except DB.IntegrityError as e:
                        cur.close()
                        conn.close()
                        conn = DB.connect(connString)
                        cur = conn.cursor()
                        print


