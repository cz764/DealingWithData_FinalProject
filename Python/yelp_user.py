import yelp_web
import mysqldao
import requests
import urllib

dbname='dwdproject'
tb_yelp_user='yelp_user'


USER_URL='http://www.yelp.com/user_details?userid='
target_user_list_query="""
    SELECT DISTINCT(userid) from log_user
    WHERE userid not in (select userid from dwdproject.yelp_user)
    """
#target_user='I-nh97QfQDXnmL4nJY4qvw'
print "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
target_user_list=mysqldao.execute_query(target_user_list_query)
for user in target_user_list:
	userid = user[0]
	url=USER_URL+str(userid)
	response=requests.get(url).text.encode('utf-8')
	linelist=str(response).split("\n")
	index=yelp_web.target_line_range(linelist, yelp_web.beginUserAttrReg, yelp_web.endUserAttrReg)
	attr_dict=yelp_web.user_attribute(linelist[index[0]:index[1]])
	attr_dict['userid']=userid
	mysqldao.insert(dbname,tb_yelp_user,[attr_dict])
	print "=======Insert user", userid

