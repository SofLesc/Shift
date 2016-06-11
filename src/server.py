#!env python3
# -*- coding: utf-8 -*-

from __future__ import print_function


from flask import Flask, render_template, request, jsonify
import ssl
import sys


context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
context.load_cert_chain('keys/server.crt', 'keys/server.key')
app = Flask("MasterCard Shift Hackathon Prototype Server")


def get_file(file_loc):
    try:
        f = open(file_loc, "r")
        ret = f.read()
        f.close()
        return ret
    except Exception as e:
        print(e)
        print("Failed to load page:" + file_loc, file=sys.stderr)
        return ""


root_page = get_file("pages/root.html")
@app.route('/')
def root_page():
    return root_page


logged_page = get_file("pages/logged.html")
@app.route('/logged')
def logged_page():
    text = ""
    try:
        text = str("tried with " + request.args['name'] + " " + request.args['last_name'])
    except:
        pass

    print("text:", text)
    print("args:", request.args)

    try:
        ret = "<!DOCTYPE html><html><head><meta charset=\"utf-8\"></head><body>" + text + "<div><class='oi'><br><b>oi sofia</body></html>"
    except:
        ret = "<!DOCTYPE html><html><head><meta charset=\"utf-8\"></head><body></body></html>"
    return ret
#    return "logado", request.args['first_name'], request.args['last_name']


app.run(host='0.0.0.0', port=8080, ssl_context=context, threaded=True, debug=True)
