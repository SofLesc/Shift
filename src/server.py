#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function

import qrcode_handler
from database import Database, Place, User, Transaction

from flask import Flask, render_template, request, jsonify, send_file, send_from_directory
import sys
import os.path


def populate():
    db = Database.Instance()
    p = Place("MASP", "Av. Paulista", "15")
    db.add_place(p.place_id, p)
    p = Place("Cristo Redentor", "Rio de Janeiro", "45")
    db.add_place(p.place_id, p)
    p = Place("Saída 1 - Shopping Dom Pedro", "Rodovia Dom Pedro", "12")
    db.add_place(p.place_id, p)
    p = Place("Pedágio 1 - Rodovia Bandeirantes", "Rodovia Bandeirantas Km 30", "2.5")
    db.add_place(p.place_id, p)

populate()

app = Flask("MasterCard Shift Hackathon Prototype Server")

SOFIA_PC = False
if SOFIA_PC:
    from OpenSSL import SSL
    context = SSL.Context(SSL.SSLv23_METHOD)
    context.use_privatekey_file('keys/server.key')
    context.use_certificate_file('keys/server.crt')
else:
    import ssl
    context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
    context.load_cert_chain('keys/server.crt', 'keys/server.key')


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


data_root_page = get_file("pages/index.html")
place_name = ""
price = -1
@app.route('/')
def root_page():
    """    user_name = ""
    user_last_name = ""
    try:
        user_id = request.args['id']
        db = Database.Instance()
        transactions = db.get_transactions()"""
    place_id = request.args.get('place_id')
    db = Database.Instance()
    print(db.root['places_list'])
    try:
        place = db.get_place(int(place_id))
        if place is not None:
               global place_name
               place_name = place.place_name
        else:
               global place_name
               place_name = "Desconhecido"
    except:
        global place_name
        place_name = "Desconhecido"
    global price
    price = request.args.get('price')

    return data_root_page.replace("$$FIRST$$", '<h3 class="section-title" id="place">' + str(place_name) + "</h3><h4 class=\"section-title alert alert-success\" id=\"price\">" + str(price) +"$</h4>").replace("$$SECOND$$", "place_id={}&price={}&".format(place_id, price))


data_place_page = get_file("pages/pay.html")


@app.route('/place')
def place_page():
    return data_place_page


data_logged_page = get_file("pages/checkout.html")


@app.route('/logged')
def logged_page():
    text = ""
    try:
        text = str("tried with " + request.args['name'] + " " + request.args['last_name'])
    except:
        pass

    print("text:", text)
    print("args:", request.args)

    #    try:
    #        ret = "<!DOCTYPE html><html><head><meta charset=\"utf-8\"></head><body>" + text + "<img src=\"https://graph.facebook.com/{}/picture?type=large\"></img></body></html>".format(request.args['id'])
    #    except:
    #        ret = "<!DOCTYPE html><html><head><meta charset=\"utf-8\"></head><body></body></html>"
    #    return ret
    #    return "logado", request.args['first_name'], request.args['last_name']

    return data_logged_page.replace("$$FIRST$$", '<img class="user" id="profile-img" alt="Buy with MasterPass" src="https://graph.facebook.com/'+ request.args['id'] +'/picture?type=large" />').replace("$$SECOND$$", '<h3 class="section-title" id="place">'+ str(place_name) +'</h3><h4 class="section-title" id="price">'+ str(price) +'$</h4>')



data_create_page = get_file("pages/create_qrcode.html")
data_create_page_redirect = get_file("pages/create_qrcode_redirect.html")


@app.route('/create')
def create_page():
    valid = True
    required = ['name', 'location', 'price']
    for i in required:
        if i not in request.args:
            valid = False
            break
    # print(request.args)
    if valid:
        # print("valid")
        # if contains all the information create the place and qrcode:
        place = Place(request.args['name'], str(request.args['location']), str(request.args['price']))
        db = Database.Instance()
        db.add_place(place.place_id, place)
        qr = qrcode_handler.QRCode(place.place_id, place.place_cost)
        qr.save_img()
        print("image saved to", qr.q_file)
        import copy
        e = copy.copy(data_create_page_redirect)
        e = e.replace("$PAGE$", "/get_image?id=" + str(qr.q_file.split('/')[-1]))
        return e
    else:
        return data_create_page


@app.route('/assets/fonts/<filename>')
def get_data0(filename):
    return send_from_directory('assets/fonts', filename)


@app.route('/assets/fonts/fontawesome/<filename>')
def get_data1(filename):
    return send_from_directory('assets/fonts/fontawesome', filename)


@app.route('/assets/css/<filename>')
def get_data2(filename):
    return send_from_directory('assets/css', filename)


@app.route('/assets/images/<filename>')
def get_data3(filename):
    return send_from_directory('assets/images', filename)


@app.route('/assets/images/blog/<filename>')
def get_data4(filename):
    return send_from_directory('assets/images/blog', filename)


@app.route('/assets/images/works/<filename>')
def get_data5(filename):
    return send_from_directory('assets/images/works', filename)


@app.route('/assets/images/ico/<filename>')
def get_data6(filename):
    return send_from_directory('assets/images/ico', filename)


@app.route('/assets/bootstrap/<filename>')
def get_data7(filename):
    return send_from_directory('assets/bootstrap', filename)


@app.route('/assets/bootstrap/fonts/<filename>')
def get_data8(filename):
    return send_from_directory('assets/bootstrap/fonts', filename)


@app.route('/assets/bootstrap/css/<filename>')
def get_data9(filename):
    return send_from_directory('assets/bootstrap/css', filename)


@app.route('/assets/bootstrap/js/<filename>')
def get_data10(filename):
    return send_from_directory('assets/bootstrap/js', filename)


@app.route('/assets/js/<filename>')
def get_data11(filename):
    return send_from_directory('assets/js', filename)


@app.route('/assets/<filename>')
def get_data12(filename):
    return send_from_directory('assets', filename)


@app.route('/<filename>')
def get_data13(filename):
    return send_from_directory('.', filename)


@app.route('/get_image')
def get_image():
    try:
        filename = "qrcode/" + request.args.get('id')
        if os.path.isfile(filename):
            return send_file(filename, mimetype='image/png')
    except:
        return send_file("bug.png", mimetype='image/png')

app.run(host='127.0.0.1', port=8080, ssl_context=context, threaded=True, debug=True)
