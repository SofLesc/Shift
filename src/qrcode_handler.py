#!/usr/bin/env python
# -*- coding: utf-8 -*-

import qrcode


class QRCode:
    def __init__(self, q_id, price):
        self.q_id = q_id
        self.price = price
        self.link = "https://172.22.41.208:8080/?place_id={}&price={}".format(q_id, price)
        self.img = None
        self.q_file = "qrcode/" + str(self.q_id) + str(self.price) + ".png"

    def gen_img(self):
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_H,
            box_size=10,
            border=4,
        )
        qr.add_data(self.link)
        qr.make(fit=True)

        self.img = qr.make_image()

    def save_img(self):
        if self.img is None:
            self.gen_img()
        self.img.save(self.q_file)

    def get_img_link(self):
        return self.q_file
