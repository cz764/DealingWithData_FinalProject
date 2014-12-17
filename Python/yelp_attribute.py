import yelp_web
import yelp_etl
import mysqldao
import requests

BIZ_URL="http://www.yelp.com/biz/"

keyword='price_range'
all_biz_id=mysqldao.select(yelp_etl.db_name, yelp_etl.tb_yelp_restaurant, ['id'])
list_biz_id=mysqldao.select(yelp_etl.db_name, yelp_etl.tb_yelp_restaurant, ['id'], [keyword], [{keyword:''}])

left_biz=len(list_biz_id)
total_biz=len(all_biz_id)
count = 0
for biz in list_biz_id:
	bizid=biz[0]
	url=BIZ_URL+bizid
	response=requests.get(url).text.encode('utf-8')
	linelist=str(response).split("\n")
	index=yelp_web.target_line_range(linelist, yelp_web.beginAttributeReg, yelp_web.endAttributeReg)
	attr_dict=yelp_web.attribute_match(linelist[index[0]:index[1]])
	attr_dict['id']=bizid
	mysqldao.update(yelp_etl.db_name, yelp_etl.tb_yelp_restaurant,\
		yelp_web.list_attribute, ['id'], [attr_dict])
	count+=1
	print bizid, 'updated', "left ", left_biz-count
