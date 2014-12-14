import mysqldao
import urllib
import json
import requests

address = """
REPLACE(
CONCAT(address1, ' ',address2, ' ', city, ' ', state,' ', zip),
'  ', ' ')
address"""

yelp_query = mysqldao.select('dwdproject', 'yelp_phone', ['phone', address, 'zip'])
address = [ [query[0], query[1]] for query in yelp_query ]
urls = []
for adr in address:
    url = 'http://maps.googleapis.com/maps/api/geocode/json?address="%s"&sensor=true' % urllib.quote(adr[1])
    urls.append(url)


resp = requests.get(urls[1])
data = json.loads(resp.text)
geo = data["results"][0]["geometry"]["location"]

data_entry = {'longitude': geo["lng"], 'latitude': geo["lat"], 'phone': address[1][0]}

mysqldao.update('dwdproject', 'yelp_phone', ['longitude', 'latitude'], ['phone'], [data_entry])
print mysqldao.select('dwdproject', 'yelp_phone', ['*'], ['phone'],[{'phone': '7188924968' }])