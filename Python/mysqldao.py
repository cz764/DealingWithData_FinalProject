"""
Please ensure that MySQL has been installed or can be connected, 
and Python for MySQL module installed successfully before running
this code.
"""

import MySQLdb as mdb
import sys

"""
Configure database connection parameters
"""
con = mdb.connect(host = 'localhost', user = 'root', passwd = '', charset='utf8');
with con:
	cursor = con.cursor()

"""
Select all the column names in a given table.
"""
def column_names(dbname,tbname):
	query="SELECT `COLUMN_NAME` \
	FROM `INFORMATION_SCHEMA`.`COLUMNS` \
	WHERE `TABLE_SCHEMA`='"+dbname+"' \
	AND `TABLE_NAME`='"+tbname+"'"
	with con:
		cur = con.cursor()
		cur.execute(query)
	column_list=[]
	for i in range(cur.rowcount):
		column_list.append(cur.fetchone())
	return column_list

"""
Creates a genric SELECT statement.
dbname=database name
tbname=table name
targetcolumns=the columns that are to be selected
keycolums=the columns used under WHERE conditions
"""
def select_statement(dbname, tbname, targetcolumns=None, keycolums=None):
	select_statement="SELECT "
	init_length=len(select_statement)
	column_list=column_names(dbname, tbname)
	if targetcolumns == None or len(targetcolumns)==0:
		select_statement+="*"
	else:
		for target in targetcolumns:
			select_statement+=target+", "
	select_statement=select_statement[:len(select_statement)-2]
	select_statement+=" FROM "+dbname+"."+tbname+" WHERE 1=1"
	if keycolums==None:
		return select_statement
	for key in column_list:
		if key[0] in keycolums:
			select_statement+=" AND "+key[0]+"=%s"
	return select_statement

"""
Use a generic SELECT statement and select values from a given table.
dbname=database name
tbname=table name
targetcolumns=the columns that are to be selected
keycolums=the columns used under WHERE conditions
keyvalues_list=the values of columns used under WHERE conditions
Sample:
select('mydb', 'yelp_phone', ['phone', 'zipcode'], ['city'], [{'city': New York'}])
will generate a SQL statement:
`SELECT phone, zipcode from mydb.yelp_phone where city = 'New York'`
to manipulate the database
"""
def select(dbname, tbname, targetcolumns=None, keycolums=None, keyvalues_list=None):
	query=select_statement(dbname, tbname, targetcolumns, keycolums)
	result_list=[]
	with con:
		cursor = con.cursor()
	if keyvalues_list==None:
		cursor.execute(query)
		for i in range(cursor.rowcount):
			result_list.append(cursor.fetchone())
		return result_list
	column_list=[]
	for i in range(cursor.rowcount):
		column_list.append(cur.fetchone())
	for kv_dict in keyvalues_list:
		v_list=[]
		for key in keycolums:
			v_list.append(kv_dict[key])
		query_parameters=tuple(v_list)
		cursor.execute(query, query_parameters)
		con.commit()
		for i in range(cursor.rowcount):
			result_list.append(cursor.fetchone())
	con.close()
	return result_list


def update_statement(dbname, tbname, updatecolumns, keycolums):
	update_statement="UPDATE "+dbname+"."+tbname+" SET "
	init_length = len(update_statement)
	column_list=column_names(dbname, tbname)
	if isinstance(updatecolumns, list):
		if len(updatecolumns) == 0:
			updatecolumns=column_list
	else:
		updatecolumns=column_list
	for column in column_list:
		c=column[0]
		if c in updatecolumns:
			update_statement+=c+"=%s, "
	if len(update_statement) == init_length:
		return ""
	update_statement=update_statement[:len(update_statement)-2]
	update_statement+=" WHERE 1=1"
	for keycolum in column_list:
		if keycolum[0] in keycolums:
			update_statement+=" AND "+keycolum[0]+"=%s"
	return update_statement

"""
updatecolumns=A list of columns that are to be updated
keycolums=A list of columns that used under WHERE as conditions
data_entry=A list of dictionary, that each one includes all the parameters for updating
Sample:
update('mydb', 'yelp_phone', ['longitude', 'latitude'], ['phone'], 
	[{'longitude':37.1674, 'latitude': 74.1134, 'phone':2015239567}])
will generate a SQL statement:
`UPDATE mydb.yelp_phone
SET longitude = 37.1674, latitude = 74.1134
WHERE phone = 2015239567`
to manipulate the database
"""
def update(dbname, tbname, updatecolumns, keycolums, data_entry):
	# with con:
	# 	cursor = con.cursor()
	query=update_statement(dbname, tbname, updatecolumns, keycolums)
	print query

	if query == "":
		return False
	if isinstance(updatecolumns, list):
		if len(updatecolumns) == 0:
			updatecolumns=column_names(dbname, tbname)
	else:
		updatecolumns=column_names(dbname, tbname)
	for data in data_entry:
		para_list = []
		for column in updatecolumns:
			para_list.append(data[column])
		for key in keycolums:
			para_list.append(data[key])
		query_parameters=tuple(para_list)
		try:
			cursor.execute(query, query_parameters)
			con.commit()
		except:
			print "====Exception.\n"+str(query_parameters)
	cursor.close()


def insert_statement(dbname,tbname):
	column_list=column_names(dbname,tbname)
	insert_query="INSERT INTO "+dbname+"."+tbname+" ("
	for column in column_list:
		insert_query+=column[0]+","
	insert_query=insert_query[0:len(insert_query)-1]
	insert_query+=") VALUES ("
	for column in column_list:
		insert_query+="%s,"
	insert_query=insert_query[:len(insert_query)-1]+")"
	return insert_query

def insert(dbname, tbname, data_entry):
	with con:
		cursor = con.cursor()
	query=insert_statement(dbname,tbname)
	column_list=column_names(dbname,tbname)
	for data in data_entry:
		data_list=[]
		for column in column_list:
			data_list.append(data[column[0]])
		query_parameters=tuple(data_list)
		try:
			cursor.execute(query, query_parameters)
			con.commit()
		except:
			print "====Exception of insertion.\n"+str(query_parameters)
	cursor.close()

def select_unique_column(dbname,tbname, columnname):
	columnname_list=[]
	unique_column="DISTINCT("+columnname+")"
	columnname_list.append(unique_column)
	tup= select(dbname, tbname, columnname_list,None,None)
	if isinstance(tup, list):
		column_value_list=[]
		for i in range(0, len(tup)):
			column_value_list.append(tup[i][0])
		return column_value_list
	else:
		return []
		
