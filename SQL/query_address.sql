select 
phone,
REPLACE(
CONCAT(address1, ' ',address2, ' ', city, ' ', state,' ', zip),
'  ', ' ')
address,
zip
from yelp_phone
WHERE (longitude = 0 or longitude is null)
and (latitude = 0 or latitude is null)