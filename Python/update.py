import mysqldao
import urllib

address = """
REPLACE(
CONCAT(address1, ' ',address2, ' ', city, ' ', state,' ', zip),
'  ', ' ')
address"""

yelp_query = mysqldao.select('yelp', 'yelp_phone', ['phone', address, 'zip'])
# address = urllib.quote(yelp_query[1][1])
yelp_query

import json
import requests

address = [ [query[0], query[1]] for query in yelp_query ]
entries = []

del address[0]

little = []
little.append(address[1])
little.append(address[2])
little.append(address[3])


import MySQLdb as mdb
import sys

con = mdb.connect(host = 'localhost', user = 'root', passwd = 'jane@nyu2013', charset='utf8');
cursor = con.cursor()

db_name = 'yelp'

update_template = """UPDATE yelp.yelp_phone 
SET longitude = %s, latitude = %s
WHERE phone = %s;"""

select_template = """SELECT phone, longitude, latitude
from yelp.yelp_phone
where phone = %s"""

for adr in address:	
	url = 'http://maps.googleapis.com/maps/api/geocode/json?address="%s"&sensor=true' % (urllib.quote(adr[1]))
	resp = requests.get(url)
	data = json.loads(resp.text)
	# print "Getting geometry for %s" % adr
	if data["results"]:
		geo = data["results"][0]["geometry"]["location"]
		entry = {'longitude': geo["lng"], 'latitude': geo["lat"], 'phone': adr[0]}
		# mysqldao.update('yelp', 'yelp_phone', ['latitude', 'longitude'], ['phone'], [entry])
		select_parameters = entry["phone"]
		cursor.execute(select_template, select_parameters)
		row = cursor.fetchall()
		lon = row[0][1]
		lat = row[0][2]
		if lon == 0 and lat == 0:
			print "the entry is %s" % entry
			update_parameters = (entry["longitude"], entry["latitude"], entry["phone"])
			cursor.execute(update_template, update_parameters)
		con.commit()

		# print mysqldao.select('yelp', 'yelp_phone', ['*'], ['phone'],[{'phone': entry["phone"]}])
		entries.append(entry)
cursor.close()


