#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# based on: http://www.zodb.org/en/latest/documentation/articles/ZODB1.html#a-simple-example


from ZODB import DB
from ZODB.FileStorage import FileStorage
from persistent import Persistent
import transaction
import time


class User(Persistent):
    def __init__(self, user_id, name, last_name):
        self.user_id = user_id
        self.name = name
        self.last_name = last_name


class Place(Persistent):
    places_count = None

    def get_place_id(cls):
        cls.places_count += 1
        return cls.places_count

    def __init__(self, place_name, place_location, place_cost):
        self.place_id = Place.get_place_id()
        self.place_name = place_name
        self.place_location = place_location
        self.place_cost = place_cost


class Transaction(Persistent):
    transaction_id = None
    
    def get_transaction_id(cls):
        cls.transaction_id += 1
        return cls.transaction_id

    def __init__(self, user_id, place_id):
        self.transaction_id = Transaction.get_transaction_id()
        self.user_id = user_id
        self.place_id = place_id
        self.time = time.time()


class Database:
    def __init__(self):
        # setup the database
        storage = FileStorage('db/database.fs')
        db = DB(storage)
        self.conn = db.open()
        self.root = self.conn.root()

        #create the mappings
        if 'user_list' not in self.root:
            self.root['user_list'] = dict()
        if 'places_list' not in self.root:
            self.root['places_list'] = dict()
        if 'transactions' not in self.root:
            self.root['transactions'] = dict()
        if 'transaction_count' not in self.root:
            self.root['transaction_count'] = 0
        if 'places_count' not in self.root:
            self.root['places_count'] = 0
        
        Transaction.transaction_id = self.root['transaction_count']
        Place.places_count = self.root['places_count']

        self.user_list = self.root['user_list']
        self.places_list = self.root['places_list']
        self.transactions = self.root['transactions']

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.root['transaction_count'] = Transaction.transaction_id
        self.root['places_count'] = Place.places_count
        transaction.commit()
        self.conn.close()

    def get_user(self, user_id):
        return self.user_list.get(user_id, None)

    def add_user(self, user_id, data):
        self.user_list[user_id] = data
        transaction.commit()

    def add_transaction(self, id, data):
        self.transactions[id] = data
        transaction.commit()

    def add_place(self, place_id, data):
        self.places_list[place_id] = data
        transaction.commit()

    def get_place(self, place_id):
        return self.places_list.get(place_id, None)

    def get_transactions(self):
        ret = list()
        for i, j in self.transactions.items():
            user = self.user_list[j[0]]
            place = self.places_list[j[1]]
            ret.append((i, user, place))
        return ret

    def commit(self):
        transaction.commit()
