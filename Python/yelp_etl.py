import yelp_api
import mysqldao
import json
import datetime
import time

API_HOST = 'api.yelp.com'
SEARCH_PATH = '/v2/search/'
TERM='restaurant'
LOCATION='New York, NY'
LIMIT=20
OFFSET=20
BUSINESS='businesses'

db_name = 'dwdproject'
tb_inspection='inspection'
tb_log_phone='extract_log_phone'
tb_log_zipcode='extract_log_zipcode'
tb_yelp_phone='yelp_phone'
tb_yelp_zipcode='yelp_zipcode'
tb_zipcode='zipcode_nyc'
tb_integration='integration'

url_params = {
        'term': TERM.replace(' ', '+'),
        'location': LOCATION.replace(' ', '+'),
        'limit': LIMIT
    }


def dic_look_up(dic, key):
    if isinstance(dic, dict):
        if key in dic:
            return dic[key]
        for k, v in dic.items():
            if isinstance(v, dict):
                return dic_look_up(v, key)

def categories_tran(lis, index):
    categories = ""
    if isinstance(lis, list):
        for sub_list in lis:
            if isinstance(sub_list, list):
                categories += sub_list[index]+", "
    length = len(categories)
    return categories[:length-2]

def display_address_tran(address_list):
    display_address = ""
    if isinstance(address_list, list):
        for item in address_list:
            display_address+= item+", "
    return display_address[:len(display_address)-2]

def search_parameter(url_params=url_params):
    return yelp_api.request(API_HOST, SEARCH_PATH, url_params=url_params)

def extract_full(url_params=url_params,limit=LIMIT):
    url_params['offset']=0
    print "Extract in full mode with parameters", url_params
    extracttime = str(datetime.datetime.now())[0:19]
    first_extract = search_parameter(url_params)
    data=json.dumps(first_extract)
    data=json.loads(data)
    total = data['total']
    zipcode='Unknown'
    if 'zipcode' in url_params:
        zipcode=url_params['zipcode']
    log_para_list = [{'extracttime':extracttime, 'total':total, 'location':url_params['location'], 'zipcode':zipcode}]
    mysqldao.insert(db_name,tb_log_zipcode,log_para_list)
    columns_list = mysqldao.column_names(db_name, tb_yelp_zipcode)
    num_extract = total / limit +1
    data_entry_list = []
    print "Total:", str(total), "extract until 1000 data"
    count=0
    for i in range(0, num_extract):
        #print "----No."+str(i+1)+" extraction"
        url_params['offset'] = i*OFFSET
        if i==49:
            break
        else:
            biz_list_i = search_parameter(url_params)[BUSINESS]
            tran_list = json_transform(biz_list_i,columns_list)
            count+=load_data_db(db_name, tb_yelp_zipcode, tran_list)
    print "Insert",count,"in the last run"

def extract_by_zipcode(url_params=url_params):
    print "====Begin extraction by zipcode."
    zip_tuple_all=mysqldao.select(db_name,tb_zipcode,['zipcode'])
    exist_zipcode_tuple = mysqldao.select_unique_column(db_name,tb_log_zipcode,'zipcode')
    for code in zip_tuple_all:
        zipcode = str(code[0])
        url_params_copy=url_params
        if zipcode not in exist_zipcode_tuple:
            url_params_copy['location']="New York, "+str(zipcode)+", NY"
            url_params_copy['zipcode']=str(zipcode)
            extract_full(url_params_copy)
        else:
            print zipcode, "existed."

def extract_by_phone(phone_list=None):
    print "====Begin extraction by phone."
    columns_list = mysqldao.column_names(db_name, tb_yelp_phone)
    biz_list=[]
    if phone_list==None:
        phone_list=[]
        temp_phone_list=mysqldao.select(db_name, tb_integration, ['PHONE'])
        for p in temp_phone_list:
            phone_list.append(p[0])
    exist_phone_list=[]
    exist_phone_tuple = mysqldao.select_unique_column(db_name,tb_log_phone,'phone')
    count = 0
    for phone in phone_list:
        phone=str(phone).replace(' ','').replace('_','')
        if len(phone) ==11:
            phone = phone[1:]
        if phone not in exist_phone_tuple:
            url_params={
            "phone":phone,
            'ywsid':'bxtstnNlHgO8c6W4X2yuYA'
            }
            biz_data = yelp_api.request(API_HOST, '/phone_search', url_params=url_params)[BUSINESS]
            if len(biz_data) != 0:
                data_phone=dic_look_up(biz_data[0],'phone')
                if data_phone == phone:
                    biz_list.append(biz_data[0])
            print "Phone:",phone,"count",len(biz_list),'data'
            tran_list=json_transform_phone(biz_list,columns_list)
            load_data_db(db_name, tb_yelp_phone, tran_list)
            extracttime = str(datetime.datetime.now())[0:19]
            log_para_list = [{'extracttime':extracttime, 'phone':phone}]
            mysqldao.insert(db_name,tb_log_phone,log_para_list)
           

def json_transform_phone(data_entry_list, columns_list):
    tran_list=[]
    for data in data_entry_list:
        tran_data={}
        for column in columns_list:
            key=column[0]
            if isinstance(data, dict):
                try:
                    if key == "categories":
                        categories=""
                        for cat_dic in data["categories"]:
                            categories+=", "+str(cat_dic["name"])
                        tran_data[key]=categories[2:]
                    elif key == "id":
                        url=data["url"]
                        tran_data[key]=url[url.rfind('/')+1:]
                    else:
                        tran_data[key] = dic_look_up(data,key)
                except:
                    print "Exception: key="+key+" in data "+str(data)
        tran_list.append(tran_data)
    return tran_list

def json_transform(data_entry_list,columns_list):
    tran_list = []
    for data in data_entry_list:
        tran_data = {}
        for column in columns_list:
            key = column[0]
            if isinstance(data, dict):
                try:
                    if key == "categories":
                        if key in data:
                            tran_data[key] = categories_tran(data[key], 0)
                        else:
                            tran_data[key] = unicode('\x80Unknown', errors='ignore')
                    elif key == "display_address":
                        location = dic_look_up(data,"location")
                        tran_data[key] = display_address_tran(location[key])
                    else:
                        tran_data[key] = dic_look_up(data,key)
                except KeyError:
                    print "----KeyError from data:\n"+str(data)+"\n-----"
        tran_list.append(tran_data)
    return tran_list


def load_data_db(dbname, tbname, data_entry_list):
    id_key='id'
    insert_list=[]
    update_list=[]
    exist_id_tuple=mysqldao.select_unique_column(dbname, tbname, id_key)
    for data in data_entry_list:
        if data[id_key] in exist_id_tuple:
            update_list.append(data)
        else:
            insert_list.append(data)
    #print 'Update exist '+str(len(update_list))+" data."
    #mysqldao.update(dbname, tbname, '', ['id'], update_list)
    #print 'Insert new '+str(len(insert_list))+" data."
    mysqldao.insert(dbname,tbname,insert_list)
    return len(insert_list)

