# file_name:	xml_server.py
# author:		lichao6
# usage:		python3 xml_server.py
# date:			2020-02-12
# description:	XML Http server example

from http.server import BaseHTTPRequestHandler, HTTPServer
import logging
import json
import xml.dom.minidom

from DbOper import DbOper

# create table tmp_ec_info(ec_id varchar(255), ec_info varchar(255));
db_conn_str = "jtxnrbs#jtxnrbs#10.19.18.67:1521/NGBOSS_TEST_11GR2"

class S(BaseHTTPRequestHandler):
	def do_HEAD(self):
		self.send_response(200)
		self.send_header('Content-type', 'text/json')
		self.end_headers()

	def do_POST(self):
		content_length = int(self.headers['Content-Length']) # <--- Gets the size of data
		post_data = self.rfile.read(content_length) # <--- Gets the data itself

		logging.info("POST request,\nPath: %s\nHeaders:\n%s\n\nBody:\n%s\n",
			str(self.path), str(self.headers), post_data.decode('utf-8'))

		self.do_HEAD()
		result = self.handle_ec(post_data)
		response = {
		        "returnCode": "0000",
		        "returnMessage": "SUCCESS",
		        "reqInfo ": "test",
		    }
		self.wfile.write(json.dumps(response).encode('utf-8'))

	def handle_ec(self, xml_data):
		dom = xml.dom.minidom.parseString(xml_data)
		EcBillEl = dom.getElementsByTagName('EcBill')[0]
		
		ecDict = {}
		ecDict['EcBill'] = EcBillEl.childNodes[0].data
		
		print("EcBill=", ecDict['EcBill'] )
		ret = self.do_insert_db(ecDict['EcBill'])

	def do_insert_db(self, ecBill):
		try:
			g_dbPool = DbOper("oracle", db_conn_str, 1)
			db_conn = g_dbPool.get_conn()
			db_cur = db_conn.cursor()
			sql_str = "insert into tmp_ec_info(ec_id, ec_info) values(:2, :3)"
			db_data = (ecBill, "test info")
			#sql_str = "select * from  tmp_ec_info"
			dbResult = db_cur.execute(sql_str, db_data)
			db_conn.commit()
			db_cur.close()
			db_conn.close()
		except Exception as e:
			logging.error("execute sql error - db:%s, sql:%s, exception: %s" % (db_conn_str, sql_str, e))
		logging.info("do_insert_db - db_result: %s" % json.dumps(dbResult))

def run():
    port = 9999
    print('starting server, port', port)

    # Server settings
    server_address = ('', port)
    httpd = HTTPServer(server_address, S)
    print('running server...')
    httpd.serve_forever()

if __name__ == '__main__':
    run()