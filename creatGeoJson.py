import psycopg2 as DB
import math
import numpy as np
import os
import json

'''Create Points Geojson '''
geofeature = {"type": "FeatureCollection",
              "features": []
              }
conn = DB.connect('dbname=urban_proj user=june')
cur = conn.cursor()
q_str = ''' select count(*),place_loc,x_lng, y_lat,trip_purpose
                    from trip,place_loc where place_loc = place_id
                    and trip_purpose in ('13','17','18','20')
                    and x_lng is not null
                    group by trip_purpose,place_loc,x_lng,y_lat
                    order by count Desc limit 2000; '''
cur.execute(q_str)
rows = cur.fetchall()
for row in rows:
    print(row)
    coor = [row[2], row[3]]
    geofeature['features'].append(
        {
            "type": "Feature",
            "properties": {
                'place_id': row[1],
                'frequent': row[0],
                'trip_purpose': row[4]
            },
            "geometry": {
                'type': 'Point',
                'coordinates': coor
            }
        }
    )
out_file = open('/Users/JNEP/project/7945_ind/locations_large.json', "w")
json.dump(geofeature, out_file)
out_file.close()

'''Create Line String '''
line_features = {"type": "FeatureCollection",
                 "features": []
                 }
conn = DB.connect('dbname=urban_proj user=june')
cur = conn.cursor()
q_str = '''         select b.income, b.house_lng, b.house_lat, b.trip_lng, b.trip_lat, b.trip_purpose from (
                    select income,
                    (select x_lng from place_loc where place_loc.place_id = household.hh_loc) as house_lng,
                    (select y_lat from place_loc where place_loc.place_id = household.hh_loc) as house_lat,
                    (select x_lng from place_loc where place_loc.place_id = trip.place_loc) as trip_lng,
                    (select y_lat from place_loc where place_loc.place_id = trip.place_loc) as trip_lat,
                    trip_purpose
                    from person,trip,household
                    where person.hh_id = trip.hh_id
                    and person.p_id = trip.p_id
                    and household.hh_id = person.hh_id
                    and trip_purpose in ('13','17','18','20') limit 30000) as b
                    where b.house_lat <> b.trip_lat
                    and b.house_lng is not null
                    and b.trip_lng is not null;'''
cur.execute(q_str)
rows_line = cur.fetchall()
for eachLine in rows_line:
    if eachLine[1] is not None and eachLine[3] is not None:
        income = eachLine[0]
        house_lng = eachLine[1]
        house_lat = eachLine[2]
        trip_lng = eachLine[3]
        trip_lat = eachLine[4]
        trip_purpose = eachLine[5]
        line_features['features'].append(
            {
                "type": "Feature",
                "properties": {
                    'income': income,
                    'trip_purpose': trip_purpose
                },
                "geometry": {
                    "type": "LineString",
                    "coordinates": [
                        [
                            house_lng,
                            house_lat
                        ],
                        [
                            trip_lng,
                            trip_lat
                        ]
                    ]
                }
            }
        )
out_income = open('/Users/JNEP/project/7945_ind/income_large.json', "w")
json.dump(line_features, out_income)
out_income.close()
