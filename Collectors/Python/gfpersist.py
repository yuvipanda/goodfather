import jsonpickle
import simplejson
import sqlite3
import os

class Persistable:

	def __maptype(self, value):
		if type(value) is dict:
			return Persistable(v)
		elif type(value) is list:
			return [self.__maptype(v) for v in value]
		else:
			return value

	def __init__(self, json):
		for k, v in json.items():
			self.__dict__[k] = self.__maptype(v)

#Inherit from this for container - eg. Blog, TweetsSearch, etc
class PersistanceContainer:

	def persist(self, item):
		self.connection.execute(
				'INSERT INTO Data VALUES (:Data)', 
				{'Data':jsonpickle.encode(item, unpickable=False)}
				)
		self.connection.commit()

	def __init__(self, filepath, createnew = True):
		fileexists = os.path.exists(filepath)
		if createnew and fileexists:
			os.remove(filepath) 
		
		self.connection=sqlite3.connect(filepath)

		if createnew: 
			self.connection.execute(r'CREATE Table Data (Data)')

#Does a streaming Read. Use for large datasets.
#Pro: Much less memory usage. Con: No in-memory caching
def read_data(filepath, streaming=False):
	conn = sqlite3.connect(filepath)
	cur = conn.cursor()
	cur.execute("SELECT * from Data")
	if streaming:
		while True:
			row = cur.fetchone()
			if row:			
				yield Persistable(simplejson.loads(row[0]))
	else:
		return [Persistable(simplejson.loads(row[0])) for row in cur.fetchall()]
