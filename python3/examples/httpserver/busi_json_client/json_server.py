# file_name:	json_server.py
# author:		lichao6
# usage:		python3 json_server.py
# date:			2020-02-13
# description:	Json Http server example

from werkzeug.wrappers import Request, Response
from werkzeug.serving import run_simple

from jsonrpc import JSONRPCResponseManager, dispatcher
import json

import logging
import sys

DEFAULT_SERV_PORT = 9998
MODULE_NAME = "JsonServ"

@dispatcher.add_method
def notify(**args):
	
	print("notify received -" + json.dumps(args))

	result = {}
	result['returnCode'] = "0000"
	result['returnMessage'] = "SUCCESS"
	result['reqInfo '] = "test info"
	
	return result

@Request.application
def application(request):
	# Dispatcher is dictionary {<method_name>: callable}
	response = JSONRPCResponseManager.handle(request.data, dispatcher)
	return Response(response.json, mimetype='application/json')

if __name__ == '__main__':
	run_simple('127.0.0.1', DEFAULT_SERV_PORT, application, threaded=True)