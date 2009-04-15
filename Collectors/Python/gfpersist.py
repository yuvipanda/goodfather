import jsonpickle
import sqlite3
import os

#Inherit from this for objects - eg. Tweet, BlogPost, Comment, etc
class Persistable:
	
	def tojson(self):
		return jsonpickle.encode(self, unpicklable=False)

#Inherit from this for container - eg. Blog, TweetsSearch, etc
class PersistanceContainer:

	def persist(self, item):
		self.connection.execute(
				'INSERT INTO Data VALUES (:Data)', 
				{'Data':item.tojson()}
				)
		self.connection.commit()

	def __init__(self, filepath, createnew = True):
		fileexists = os.path.exists(filepath)
		if createnew and fileexists:
			os.remove(filepath) 
		
		self.connection=sqlite3.connect(filepath)

		if createnew: 
			self.connection.execute(r'CREATE Table Data (Data)')


	def __del__(self):
		#clean up the connection when the app stops.
		#No idea why this throws
		#self.connection.close()
		pass
