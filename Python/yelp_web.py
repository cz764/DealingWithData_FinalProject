import re
import urllib
import mysqldao
import HTMLParser
import requests
import sys
reload(sys)
sys.setdefaultencoding('utf-8') 

beginReviewReg='<div class="review-list">'
useridReg = 'a class="user-display-name" href="/user_details\?userid'
reviewReg= '<p itemprop="description" .*>.*</p>'
reviewDateReg='<meta itemprop="datePublished" content=.*>'
ratingReg='<meta itemprop="ratingValue" content="'
checkinReg='<i  class="i ig-common i-checkin-burst-blue-small-common"></i>.* check-ins</span>'
usefulReg='<span class="vote-type">Useful</span>'
funnyReg='<span class="vote-type">Funny</span>'
coolReg='<span class="vote-type">Cool</span>'
countReg='<span class="count">'
endReviewReg='<div class="review-pager">'

beginAttributeReg='<h3 class="offscreen">Business info summary</h3>'
priceRangeReg='<span class="business-attribute price-range.*>.*</span>'
priceDescReg='<dd class="nowrap price-description">'
attributeReg='<dt class="attribute-key">$'
endAttributeReg='<div class="media-block clearfix first-to-review ywidget">'

list_attribute=["TakesReservations","Delivery","Take-out","AcceptsCreditCards"
,"GoodForDinner","ParkingStreet","BikeParking","WheelchairAccessible","GoodforKids"
,"GoodforGroups","AttireCasual","AmbienceTrendy","iseLevelAverage"
,"AlcoholFullBar","OutdoorSeating","Wi-Fi","HasTV","DogsAllowed","WaiterService"
,"Caters","price_range","price_description"]


dbname='dwdproject'
tb_yelp_reivew='yelp_review'
tb_yelp_user='yelp_user'

columns_tuple=mysqldao.column_names('dwdproject', tb_yelp_reivew)

def target_line_range(linelist, beginReg, endReg):
	begin=0
	end=0
	size=len(linelist)
	for i in xrange(0, size):
		try:
			line=HTMLParser.HTMLParser().unescape(linelist[i]).encode('utf-8')
			if re.search(beginReg, line):
				begin=i
				break
		except:
			q=1
	for i in xrange(0, size):
		try:
			_i = size-i
			line=HTMLParser.HTMLParser().unescape(linelist[_i]).encode('utf-8')
			if re.search(endReg, line):
				end= _i
				break
		except:
			q=1
	return (begin, end)


def accross_line_split(linelist, beginindex, endReg):
	result=''
	for i in xrange(beginindex, len(linelist)):
		if re.search(endReg, linelist[i]):
			result= linelist[i-1]
			break
	return result.strip()

def review_match(linelist, bizid):
	review_dict_list=[]
	review_dict={"bizid":bizid, "checkins":0}
	checkins=0
	for i in xrange(0, len(linelist)):
		#try:
		if True:
			line=linelist[i]
			if re.search(useridReg, line):
				review_dict["userid"]=inline_split(line, "userid=", '" data-hovercard')
			elif re.search(reviewReg, line):
				review=str(inline_split(line, ">", "</p>")).replace('<br>','\n')
				review_dict["review"]=HTMLParser.HTMLParser().unescape(review)
			elif re.search(reviewDateReg, line):
				review_dict["review_date"]=inline_split(line, 'content="', '">')
			elif re.search(checkinReg, line):
				review_dict["checkins"]=inline_split(line,'</i>', 'check-ins').strip()
			elif re.search(ratingReg, line):
				review_dict["rating"]=inline_split(line, 'content="', '">')
			elif re.search(usefulReg, line):
				review_dict["useful"]=review_count_split(i+1, linelist)
			elif re.search(funnyReg, line):
				review_dict["funny"]=review_count_split(i+1, linelist)
			elif re.search(coolReg, line):
				review_dict["cool"]=review_count_split(i+1, linelist)
				if check_put_dict(review_dict, columns_tuple):
					review_dict_list.append(review_dict)
				review_dict={"bizid":bizid, "checkins":0}
			else:
				continue
		#except:
		#	q=1
	return review_dict_list

yelp_user_columns=mysqldao.column_names(dbname, tb_yelp_user)
list_user_attr=[]
for t in yelp_user_columns:
	list_user_attr.append(t[0])

beginUserAttrReg='<img alt="Photo of.*" class="photo-box-img"'
userTaglineReg='<p id="user_tagline">.*</p>'
userFriendsReg='<a href="/user_details_friends\?userid=.*".*</i>.*Friends</a>'
userReviewCountReg='<a href="/user_details_reviews_self\?userid=.*</i>.*Reviews</a>'
userEliteReg='<ul id="elite-badges">' ## Since
userReviewVoteReg='</i>.*Review.*votes:<br>.*Useful.*Funny.*Cool</p>'
LocationReg='<span class="highlight2">Location</span>'
YelpingSinceReg='<span class="highlight2">Yelping.*Since.*</span>'
ThingsILoveReg='<span class="highlight2">Things.*I.*Love.*</span>'
MyHometownReg='<span class="highlight2">My.*Hometown</span>'
endUserAttrReg='</i>.*Flag.*this.*profile</a>'

def user_attribute(linelist):
	attr_dict={}
	for attr in list_user_attr:
		attr_dict[attr]='0'
	attr_dict["user_tagline"]=''
	attr_dict["Elite"]=False
	attr_dict["Hometown"]=''
	attr_dict["Location"]=''
	attr_dict["ThingsILove"]=''
	attr_dict["YelpingSince"]=''

	for i in xrange(0, len(linelist)):
		line=linelist[i]
		try:
			if re.search(userTaglineReg, line):
				attr_dict["user_tagline"]=inline_split(line, '">', "</p>")
			elif re.search(userFriendsReg, line):
				attr_dict["Friends"]=inline_split(line, '</i>','Friends</a>').strip()
			elif re.search(userReviewCountReg, line):
				attr_dict["ReviewCount"]=inline_split(line, '</i>', 'Reviews').strip()
			elif re.search(userEliteReg, line):
				attr_dict["Elite"]="True"
			elif re.search(userReviewVoteReg, line):
				line=line.replace(',','').replace(' ','')
				attr_dict["Useful"]=inline_split(line, '<br>','Useful')
				attr_dict["Funny"]=inline_split(line, 'Useful','Funny')
				attr_dict["Cool"]=inline_split(line, 'Funnyand','Cool')
			elif re.search(LocationReg, line):
				Location=inline_split(linelist[i+1], "<p>", '</p>')
				attr_dict["Location"]=mulit_line_search(Location, linelist, i+1, '</p>')
			elif re.search(YelpingSinceReg, line):
				YelpingSince = inline_split(linelist[i+1], "<p>","</p>")
				attr_dict["YelpingSince"]=mulit_line_search(YelpingSince, linelist, i+1, '</p>')
			elif re.search(ThingsILoveReg, line):
				ThingsILove = inline_split(linelist[i+1], "<p>","</p>")
				attr_dict["ThingsILove"]=mulit_line_search(ThingsILove, linelist, i+1, '</p>')
			elif re.search(MyHometownReg, line):
				MyHometown = inline_split(linelist[i+1], "<p>","</p>")
				attr_dict["MyHometown"]=mulit_line_search(MyHometown, linelist, i+1, '</p>')

		except:
			q=1

	return attr_dict

def mulit_line_search(target, linelist, beginindex, endReg):
	while not target:
		target=accross_line_split(linelist, beginindex, endReg)

	return target

def attribute_match(linelist):
	attr_dict={}
	for attr in list_attribute:
		attr_dict[attr]="Unknown"
	for i in xrange(0, len(linelist)):
		line=linelist[i]
		try:
			if re.search(priceRangeReg, line):
				attr_dict['price_range']=inline_split(line, '">', "</span>")
			elif re.search(priceDescReg, line):
				attr_dict['price_description']=accross_line_split(linelist, i+1, '</dd>')
			elif re.search(attributeReg, line):
				attrName=accross_line_split(linelist, i+1, '</dt>')
				attrValue=accross_line_split(linelist, i+1, '</dd>')
				attr_dict[attrName]=attrValue
		except:
			q=1
	return attr_dict


def check_put_dict(data_dict, columns_tuple):
	for column in columns_tuple:
		key = column[0]
		if key in data_dict:
			continue
		else:
			return False
	return True


def review_count_split(index, linelist):
	count=0
	if index<= len(linelist):
		line = linelist[index]
		if re.search(countReg, line):
			line=line.strip()
			count = inline_split(line,'count">', '</')
	if not count:
		count = 0
	return count

def inline_split(line, beginword, endword):
	begin= int(line.find(beginword))+len(beginword)
	end = int(line.find(endword))
	return line[begin:end]
"""
bizid="the-cuban-restaurant-and-bar-hoboken-2"
url="http://www.yelp.com/biz/the-cuban-restaurant-and-bar-hoboken-2"
response=requests.get(url).text.encode('utf-8')
linelist = str(response).split("\n")
index=target_line_range(linelist, beginReviewReg, endReviewReg)
reviewlist=linelist[index[0]:index[1]]
review_match(reviewlist, bizid)
"""