# file_name:	xml_client.py
# author:		lichao6
# usage:		python3 xml_client.py
# date:			2020-02-12
# description:	XML Http client example

import requests

def main():
	url = "http://localhost:9999/"
	headers = {"Content-Type": "text/xml"}

	body = '<?xml version="1.0" encoding="UTF-8"?>\
		<ProvBOSS>\
			<ECBizInfo>\
				<EcBill>1111</EcBill>\
				<OprCode>11</OprCode>\
			</ECBizInfo>\
		</ProvBOSS>'

	response = requests.post(url, data=body, headers=headers)

	print("result: %s" % response.text)

if __name__ == "__main__":
	main()