#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function


from flask import Flask, render_template, request, jsonify, send_file
import sys
import os.path

from OpenSSL import SSL
context = SSL.Context(SSL.SSLv23_METHOD)
context.use_privatekey_file('keys/server.key')
context.use_certificate_file('keys/server.crt')

app = Flask("MasterCard Shift Hackathon Prototype Server")


def get_file(file_loc):
    try:
        f = open(file_loc, "r")
        ret = f.read()
        f.close()
        return ret
    except Exception as e:
        print(e)
        print("Failed to load page: " + file_loc, file=sys.stderr)
        return "<font size=16>This page is missing on the server: " + file_loc


data_root_page = get_file("pages/root.html")
@app.route('/')
def root_page():
    return data_root_page


data_place_page = get_file("pages/place.html")
@app.route('/place')
def place_page():
    return data_place_page


data_logged_page = get_file("pages/logged.html")
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
        ret = "<!DOCTYPE html><html><head><meta charset=\"utf-8\"></head><body>" + text + "<img src=\"https://graph.facebook.com/{}/picture?type=large\"></img></body></html>".format(request.args['id'])
    except:
        ret = "<!DOCTYPE html><html><head><meta charset=\"utf-8\"></head><body></body></html>"
    return ret
#    return "logado", request.args['first_name'], request.args['last_name']


@app.route('/get_image')
def get_image():
    try:
        filename = "qrcode/" + request.args.get('id')
        if os.path.isfile(filename):
            return send_file(filename, mimetype='image/png')
    except:
        return send_file("bug.png", mimetype='image/png')


app.run(host='0.0.0.0', port=8080, ssl_context=context, threaded=True, debug=True)
