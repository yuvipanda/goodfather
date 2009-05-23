import simplejson
import sqlite3
import os
from datetime import datetime
import dateutil.parser

class Persistable:

    def __reverse_maptype(self, value):
        if isinstance(value, dict):
            if value.has_key('__type__'):
                if value['__type__'] == 'datetime':
                    return dateutil.parser.parse(value['__value__'])
            else:
                return Persistable(value)
        elif isinstance(value, list):
            return [self.__reverse_maptype(v) for v in value]
        else:
            return value

    def __maptype(self, value):
        if isinstance(value, list):
            return [self.__maptype(v) for v in value]
        elif isinstance(value, Persistable):
            return Persistable.tojson()
        elif isinstance(value, datetime):
            return {
                    '__type__':'datetime',
                    '__value__':value.isoformat()
                    }
        else:           
            return unicode(value)

    def tojson(self):
        return simplejson.dumps(
                dict( [ (k, self.__maptype(v)) 
                        for k, v in self.__dict__.items()
                        ]))


    def __init__(self, json=None):
        if json:
            for k, v in json.items():
                self.__dict__[k] = self.__reverse_maptype(v)

class MetaDict():
    def __init__(self, connection, cursor):
        self.connection = connection
        self.cursor = cursor

    def __getitem__(self, key):
        self.cursor.execute("SELECT Value FROM Meta")
        row = self.cursor.fetchone()
        if row:
            return row[0]
        else:
            raise KeyError

    def __setitem__(self, key, value):
        self.cursor.execute('SELECT Key FROM Meta WHERE Key = ?', (key, ))
        if self.cursor.fetchone():
            self.cursor.execute(
                    'UPDATE Meta SET Value = ? WHERE Key = ?', 
                    (value, key )
                    )
        else:
            self.cursor.execute(
                    "INSERT INTO Meta VALUES (?, ?)", 
                    (key, value,)
                    )
        self.connection.commit()

    def __delitem__(self, key):
        self.cursor.execute(
                "DELETE FROM Meta WHERE Key = ?",
                (key,)
                )
        self.cursor.commit()


#Inherit from this for container - eg. Blog, TweetsSearch, etc
class PersistanceContainer:

    def persist(self, key, item):
        self.cursor.execute(
                'INSERT INTO Data VALUES (?, ?)', 
                (key, item.tojson(),)               
                )
        self.connection.commit()

    def has_key(self, key):
        self.cursor.execute(
                'SELECT Key FROM Data WHERE Key=?',
                (key, )
                )
        if self.cursor.fetchone():
            return True
        else:
            return False
    
    def get(self, key):
        self.cursor.execute(
                'SELECT Key, Data FROM Data WHERE Key=?',
                (key, )
                )
        row = self.cursor.fetchone()
        if row:
            return Persistable(simplejson.loads(row[1]))
        else:
            return None

    def __init__(self, filepath, createnew = False):
        fileexists = os.path.exists(filepath)
        if createnew and fileexists:
            os.remove(filepath) 
        
        self.connection=sqlite3.connect(database=filepath)
        self.cursor = self.connection.cursor()

        if createnew or not fileexists: 
            self.cursor.execute(r'CREATE TABLE Data (Key, Data)')
            self.cursor.execute(r'CREATE TABLE Meta (Key, Value)')          
            self.cursor.execute(r'CREATE INDEX KeyIndex ON Data (Key)')
            self.cursor.execute(r'CREATE INDEX MetaIndex ON Meta (Key)')
            self.connection.commit()

        self.Meta = MetaDict(self.connection, self.cursor)

    def read_all(self):
        self.cursor.execute("SELECT Data from Data")
        while True:
            row = self.cursor.fetchone()
            if row:         
                yield Persistable(simplejson.loads(row[0]))
            else:
                break
