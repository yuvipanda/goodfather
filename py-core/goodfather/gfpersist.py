import jsonpickle
import simplejson
import sqlite3
import os

class Persistable:

	def __maptype(self, value):
		if type(value) is dict:
			return Persistable(value)
		elif type(value) is list:
			return [self.__maptype(v) for v in value]
		else:
			return value

	def __init__(self, json=None):
		if json:
			for k, v in json.items():
				self.__dict__[k] = self.__maptype(v)

#Inherit from this for container - eg. Blog, TweetsSearch, etc
class PersistanceContainer:

	def persist(self, key, item):
		self.cursor.execute(
				'INSERT INTO Data VALUES (?, ?)', 
				(key, jsonpickle.encode(item, unpickable=True),)
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
			self.cursor.execute(r'CREATE INDEX KeyIndex ON Data (Key)')
			self.connection.commit()

#Does a streaming Read. Use for large datasets.
#Pro: Much less memory usage. Con: No in-memory caching
def read_streaming(filepath):
	conn = sqlite3.connect(database=filepath)
	cur = conn.cursor()
	cur.execute("SELECT Data from Data")
	#if streaming:
	while True:
		row = cur.fetchone()
		if row:			
			yield Persistable(simplejson.loads(row[0]))
		else:
			break

#Does a all-at once Read. Loads all the objects into memory
def read_all(filepath):
	conn = sqlite3.connect(database=filepath)
	cur = conn.cursor()
	cur.execute("SELECT Data from Data")
	return [Persistable(simplejson.loads(row[0])) for row in cur.fetchall()]
