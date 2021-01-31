# file_name:	json_client.py
# author:		lichao6
# usage:		python3 json_client.py
# date:			2020-02-13
# description:	Json Http client example

import requests
import json
import logging
import cx_Oracle

db_conn_str = "jtxnrbs/jtxnrbs@10.19.18.67:1521/NGBOSS_TEST_11GR2"
url = "http://localhost:9998/DataExpireNotify"
headers = {'content-type': 'application/json'}

def main():

	try:
		db_conn = conn = cx_Oracle.connect(db_conn_str)
		sql_str = "select ec_id from tmp_ec_info"
		cursor = conn.cursor()
		cursor.execute(sql_str)
		dbResult = cursor.fetchall()
		cursor.close()
		conn.close()
		printf("Db query result - " + json.dumps(dbResult))
	except Exception as e:
		print("execute sql error - exception: %s".format(e))

	body = {}
	body['busiCode'] = "DATA_EXPIRE_NOTIFY"	
	body['version']	= "1.0"
	body['reqInfo']	= []
	for row in dbResult:
		reqInfo = {}
		reqInfo['vaspId'] = row[0]
		reqInfo['cdrType'] = 1
		reqInfo['expireDate'] = "20191201000000"
		body['reqInfo'].append(reqInfo)	
	
	print("Body = " + json.dumps(body))	

	# Example query method
	payload = {
		"method": "notify",
		"params": body,
		"jsonrpc": "2.0",
		"id": 0,
	}

	print("request: %s" % json.dumps(payload))
	response = requests.post(
		url, data=json.dumps(payload), headers=headers).json()

	print("result: %s" % json.dumps(response))

if __name__ == "__main__":
	main()