1. ����
	Python 3.x
	Python����б� http.server, werkzeug, json, jsonrpc, xml.dom.minidom, cx_Oracle
	
2. ����
	esop_xml_server		-	λ�û��ض�ESOP�ṩ��Http���������� ����XML��ʽ���󣬷���json��ʽ��Ӧ�� ���ݲ������ݿ�
	busi_json_client 	-	λ�û��ض�ҵ��ƽ̨ͬ�����ݵ�Http�ͻ��������� �����ݿ��ȡ���ݣ�����json��ʽ����ҵ��ƽ̨��Ӧhttp����
	

3. XML��ʽHTTP����
	1). ����xml_server.py����������db_conn_str
	2). �����ݿ��У��������Ա� sql��xml_server��ע�ͣ� ʵ���ֶοɸ����������
	3). ����python3 xml_server.py
	4). ����python3 xml_client.py
	
4. JSON��ʽHTTP����
	1). ����json_client.py����������db_conn_str
	2). ���н���ο� 
	request: {"method": "notify", "params": {"busiCode": "DATA_EXPIRE_NOTIFY", "version": "1.0", "reqInfo": [{"vaspId": "12345", "cdrType": 1, "expireDate": "20191201000000"}, {"vaspId": "12345", "cdrType": 1, "expireDate": "20191201000000"}, {"vaspId": "1234", "cdrType": 1, "expireDate": "20191201000000"}, {"vaspId": "12345", "cdrType": 1, "expireDate": "20191201000000"}]}, "jsonrpc": "2.0", "id": 0}
	result: {"result": {"returnCode": "0000", "returnMessage": "SUCCESS", "reqInfo ": "test info"}, "id": 0, "jsonrpc": "2.0"}	