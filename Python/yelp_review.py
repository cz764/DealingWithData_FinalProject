import yelp_web
import mysqldao
import requests
import urllib

dbname='dwdproject'
tb_log_review='log_review'
tb_yelp_review='yelp_review'
BIZ_URL="http://www.yelp.com/biz/"
PAGE_OFFSET="?start="
PAGE_LIMIT=40
query="""
SELECT bizid FROM dwdproject.log_review WHERE finish = False"""
print "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
list_biz_id=mysqldao.execute_query(query)

def get_review_html(bizid, start):
	url=BIZ_URL+bizid+PAGE_OFFSET+str(start)
	print url
	response=requests.get(url).text.encode('utf-8')
	linelist = str(response).split("\n")
	index=yelp_web.target_line_range(linelist, yelp_web.beginReviewReg, yelp_web.endReviewReg)
	reviewlist=linelist[index[0]:index[1]]
	review_dict_list=yelp_web.review_match(reviewlist, bizid)
	extracted=len(review_dict_list)
	if extracted > 0:
		mysqldao.insert(dbname,tb_yelp_review,review_dict_list)
	return extracted

def extract_by_bizid(bizid, existed):
	print "==========Begin extract for ", bizid
	next = True
	while next:
		extracted=get_review_html(bizid, existed)
		if extracted > 0:
			print "Insert", extracted
			existed+=extracted
			if extracted < PAGE_LIMIT:
				next = False
		else:
			next = False
	return extracted

for biz in list_biz_id:
	bizid=biz[0]
	query="DELETE FROM dwdproject.yelp_review WHERE bizid ='" + bizid +"'"
	mysqldao.execute_query(query)
	extract_by_bizid(bizid, 0)
	query="UPDATE dwdproject.log_review SET finish = True WHERE bizid ='" + bizid +"'"
	mysqldao.execute_query(query)
	print "----------Finish extract for ", bizid

