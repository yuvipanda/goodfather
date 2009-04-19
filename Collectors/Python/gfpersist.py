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

	def persist(self, item):
		self.cursor.execute(
				'INSERT INTO Data VALUES (?)', 
				(jsonpickle.encode(item, unpickable=False),)
				)
		self.connection.commit()

	def __init__(self, filepath, createnew = True):
		fileexists = os.path.exists(filepath)
		if createnew and fileexists:
			os.remove(filepath) 
		
		self.connection=sqlite3.connect(database=filepath)
		self.cursor = self.connection.cursor()

		if createnew: 
			self.cursor.execute(r'CREATE Table Data (Data)')

#Does a streaming Read. Use for large datasets.
#Pro: Much less memory usage. Con: No in-memory caching
def read_streaming(filepath, streaming=False):
	conn = sqlite3.connect(database=filepath)
	cur = conn.cursor()
	cur.execute("SELECT * from Data")
	#if streaming:
	while True:
		row = cur.fetchone()
		if row:			
			yield Persistable(simplejson.loads(row[0]))

#Does a all-at once Read. Loads all the objects into memory
def read_all(filepath):
	conn = sqlite3.connect(database=filepath)
	cur = conn.cursor()
	cur.execute("SELECT * from Data")
	return [Persistable(simplejson.loads(row[0])) for row in cur.fetchall()]
