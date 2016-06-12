#!/usr/bin/env python
# -*- coding: utf-8 -*-

# based on: http://www.zodb.org/en/latest/documentation/articles/ZODB1.html#a-simple-example


import transaction
import time
import os


class User:
    def __init__(self, user_id, name, last_name):
        self.user_id = user_id
        self.name = name
        self.last_name = last_name


class Place:
    def __init__(self, place_name, place_location, place_cost):
        db = Database.Instance()
        self.place_id = db.get_place_id()
        self.place_name = place_name
        self.place_location = place_location
        self.place_cost = place_cost


class Transaction:
    def __init__(self, user_id, place_id, price):
        db = Database.Instance()
        self.transaction_id = db.get_transaction_id()
        self.user_id = user_id
        self.place_id = place_id
        self.price = price
        self.time = time.time()


class Singleton:
    """
    A non-thread-safe helper class to ease implementing singletons.
    This should be used as a decorator -- not a metaclass -- to the
    class that should be a singleton.

    The decorated class can define one `__init__` function that
    takes only the `self` argument. Other than that, there are
    no restrictions that apply to the decorated class.

    To get the singleton instance, use the `Instance` method. Trying
    to use `__call__` will result in a `TypeError` being raised.

    Limitations: The decorated class cannot be inherited from.

    """

    def __init__(self, decorated):
        self._decorated = decorated

    def Instance(self):
        """
        Returns the singleton instance. Upon its first call, it creates a
        new instance of the decorated class and calls its `__init__` method.
        On all subsequent calls, the already created instance is returned.

        """
        try:
            return self._instance
        except AttributeError:
            self._instance = self._decorated()
            return self._instance

    def __call__(self):
        raise TypeError('Singletons must be accessed through `Instance()`.')

    def __instancecheck__(self, inst):
        return isinstance(inst, self._decorated)


@Singleton
class Database:
    def __init__(self):
        print("starting")
        # setup the database
        if not os.path.isdir('db'):
            os.mkdir('db')

        """storage = FileStorage('db/database.fs')
        db = DB(storage)
        self.conn = db.open()
        self.root = self.conn.root()
"""
        self.root = dict()
        # create the mappings
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

        #transaction.commit()


    def get_transaction_id(self):
        self.root['transaction_count'] += 1
        transaction.commit()
        return self.root['transaction_count']

    def get_place_id(self):
        self.root['places_count'] += 1
        transaction.commit()
        return self.root['places_count']

    def __del__(self):
        pass
        #transaction.commit()
        #self.conn.close()

    def get_user(self, user_id):
        return self.user_list.get(user_id, None)

    def add_user(self, user_id, data):
        self.root['user_list'][user_id] = data
        transaction.commit()

    def add_transaction(self, t_id, data):
        self.root['transactions'][t_id] = data
        transaction.commit()

    def add_place(self, place_id, data):
        self.root['places_list'][place_id] = data
        transaction.commit()

    def get_place(self, place_id):
        return self.root['places_list'].get(place_id, None)

    def get_transactions(self):
        ret = list()
        for i, j in self.root['transactions'].items():
            user = self.root['user_list'][j[0]]
            place = self.root['places_list'][j[1]]
            ret.append((i, user, place))
        return ret

    def commit(self):
        transaction.commit()
