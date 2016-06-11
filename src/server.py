#!env python

from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

page = open("pages/root.html", "r").read()

@app.route('/')
def hello_world():
	try:
		print "name", request.args['name'], "\nid:", request.args['id']
	except:
		pass
	return page

@app.route('/logged')
def logged_page():
	text = ""
	try:
		text = str("tried with " + request.args['name'] + " " + request.args['last_name'])
	except:
		pass

	print "text:", text
	print "args:", request.args

	try:
		ret = "<!DOCTYPE html><html><head><meta charset=\"utf-8\"></head><body>" + text + "<div><class='oi'><br><b>oi sofia</body></html>"
	except:
		ret = "<!DOCTYPE html><html><head><meta charset=\"utf-8\"></head><body></body></html>"
	return ret
#	return "logado", request.args['first_name'], request.args['last_name']

import ssl
context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
context.load_cert_chain('keys/server.crt', 'keys/server.key')

app.run(host='0.0.0.0', port=8080, ssl_context=context, threaded=True, debug=True)
