1. 环境
	Python 3.x
	Python插件列表： http.server, werkzeug, json, jsonrpc, xml.dom.minidom, cx_Oracle
	
2. 介绍
	esop_xml_server		-	位置基地对ESOP提供的Http服务样例， 接收XML格式请求，返回json格式响应， 内容插入数据库
	busi_json_client 	-	位置基地对业务平台同步数据的Http客户端样例， 从数据库读取内容，发送json格式请求到业务平台对应http服务
	

3. XML格式HTTP服务
	1). 调整xml_server.py中数据连接db_conn_str
	2). 到数据库中，建立测试表， sql见xml_server中注释， 实际字段可根据需求调整
	3). 运行python3 xml_server.py
	4). 运行python3 xml_client.py
	
4. JSON格式HTTP服务
	1). 调整json_client.py中数据连接db_conn_str
	2). 运行结果参考 
	request: {"method": "notify", "params": {"busiCode": "DATA_EXPIRE_NOTIFY", "version": "1.0", "reqInfo": [{"vaspId": "12345", "cdrType": 1, "expireDate": "20191201000000"}, {"vaspId": "12345", "cdrType": 1, "expireDate": "20191201000000"}, {"vaspId": "1234", "cdrType": 1, "expireDate": "20191201000000"}, {"vaspId": "12345", "cdrType": 1, "expireDate": "20191201000000"}]}, "jsonrpc": "2.0", "id": 0}
	result: {"result": {"returnCode": "0000", "returnMessage": "SUCCESS", "reqInfo ": "test info"}, "id": 0, "jsonrpc": "2.0"}	