import simplejson
import sqlite3
import os
from datetime import datetime
import dateutil.parser

from pymongo import Connection

class Persistable:
    def __reverse_maptype(self, value):
        if isinstance(value, dict):
            return Persistable(value)
        elif isinstance(value, list):
            return [self.__reverse_maptype(v) for v in value]
        else:
            return value

    def __maptype(self, value):
        if isinstance(value, list):
            return [self.__maptype(v) for v in value]
        elif isinstance(value, Persistable):
            return value.tojson()
        elif isinstance(value, str):
            return unicode(value, encoding='UTF-8')
        else:           
            return value

    def to_dict(self):
        return dict([(k, self.__maptype(v)) 
                     for k, v in self.__dict__.items()
                     ])


    def __init__(self, dict=None):
        if dict:
            for k, v in json.items():
                self.__dict__[k] = self.__reverse_maptype(v)


#Inherit from this for container - eg. Blog, TweetsSearch, etc
class PersistanceContainer:
    def persist(self, key, item):
        to_insert = item.to_dict()
        to_insert['__key'] = key
        self._collection.insert(to_insert)

    def get(self, key):
        return self._collection.find_one({'__key':key})
        
    def __init__(self, name, collection):
        self._conn = Connection()
        self._db = self._conn[name]
        self._collection = self._db[collection]


