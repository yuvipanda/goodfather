from datetime import datetime
from xml.etree import ElementTree
import sqlite3
import os

class TwitterSearch:

	def __init__(self,filepath,createnew=True):
		exists = os.path.exists(filepath)
		if createnew==False:
			if exists:
				self.connection=sqlite3.connect(filepath)
			else:
				self.connection=sqlite3.connect(filepath)
				createPostsSQL = r'CREATE TABLE Data (Data)'		
				self.connection.execute(createPostsSQL)
		else:
			if exists:
				os.remove(filepath)
			self.connection=sqlite3.connect(filepath)
			createPostsSQL = r'CREATE TABLE Data (Data)'		
			self.connection.execute(createPostsSQL)

	def persist(self,item):
		self.connection.execute('INSERT INTO Data VALUES (:data)',{'data':ElementTree.tostring(item.toxml())})
		self.connection.commit()
	
	def __del__(self):
		self.connection.close()



class Tweet:
	def __init__(self):
		
		self.IconURL = u''
		
		self.Text = u''
		
		self.Author = u''
		
		self.ID = u''
		
		self.Language = u''
		
		self.AuthorID = u''
		
		self.Published = datetime(1970,1,1)
		
		self.ReplyToUser = u''
		

		

	def toxml(self):
		element = ElementTree.Element('Tweet')
		
		ElementTree.SubElement(element,'IconURL').text = self.IconURL
		
		ElementTree.SubElement(element,'Text').text = self.Text
		
		ElementTree.SubElement(element,'Author').text = self.Author
		
		ElementTree.SubElement(element,'ID').text = self.ID
		
		ElementTree.SubElement(element,'Language').text = self.Language
		
		ElementTree.SubElement(element,'AuthorID').text = self.AuthorID
		
		ElementTree.SubElement(element,'Published').text = self.Published.isoformat()
		
		ElementTree.SubElement(element,'ReplyToUser').text = self.ReplyToUser
		

		
		
		return element



