import mysqldao
import urllib
import time

address = """
REPLACE(
CONCAT(address1, ' ',address2, ' ', city, ' ', state,' ', zip),
'  ', ' ')
address"""

yelp_query = mysqldao.select('yelp', 'yelp_phone', ['phone', address, 'zip'], ['longitude', 'latitude'], [{'longitude': 0, 'latitude': 0}])
# address = urllib.quote(yelp_query[1][1])
print len(yelp_query)

import json
import requests

address = [ [query[0], query[1]] for query in yelp_query]
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
from yelp.yelp_phone;"""

for adr in address:	
	url = """http://maps.googleapis.com/maps/api/geocode/json?address="%s"&sensor=true""" % (urllib.quote(adr[1]))
	print "url: %s" % url
	resp = requests.get(url)
	data = json.loads(resp.text)
	print "Getting geometry for %s" % adr
	print "~~~result status %s " % (data["status"])
	status = data["status"]
	if status == "OVER_QUERY_LIMIT":		
		continue
	if data["results"]:
		geo = data["results"][0]["geometry"]["location"]
		phone = int(adr[0])
		# entry = {'%s' % phone: {'longitude': geo["lng"], 'latitude': geo["lat"]}}
		entry = {'longitude': geo["lng"], 'latitude': geo["lat"], 'phone': phone}
		entries.append(entry)
		print "updating %s" % entry
		update_parameters = (entry["longitude"], 
			entry["latitude"],
			entry["phone"])
		cursor.execute(update_template, update_parameters)
		con.commit()
	time.sleep(1)


print "!!!!!!!!!!done getting all geo locations for all entries!!!!!!!!!"
# cursor.execute(select_template)
# rows = cursor.fetchall()
# for row in rows:
# 	phone = row[0][0]
# 	lon = row[0][1]
# 	lat = row[0][2]
# 	if lon == 0 and lat == 0:
# 		print "updating %s" % row
# 		update_parameters = (entries["%s" % phone]["longitude"], 
# 			entries["%s" % phone]["latitude"],
# 			phone)
# 		print update_parameters
# 		cursor.execute(update_template, update_parameters)
# 	con.commit()
cursor.close()


