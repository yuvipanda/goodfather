

from datetime import datetime
from xml.etree import ElementTree
import sqlite3

class Blog:

	def __init__(self,filepath):
		createPostsSQL = r'CREATE TABLE Data (Data)'
		self.connection = sqlite3.connect(filepath)
		c = self.connection.cursor()
		c.execute(createPostsSQL)
	
	def persist(self,item):
		self.connection.execute('INSERT INTO Data VALUES (:data)',{'data':ElementTree.tostring(item.toxml())})
		self.connection.commit()
	
	def __del__(self):
		self.connection.close()



class Post:
	def __init__(self):
		
		self.Content = u''
		
		self.Permalink = u''
		
		self.Author = u''
		
		self.AuthorLink = u''
		
		self.Title = u''
		
		self.Published = datetime(1970,1,1)
		

		
		self.Tags = []
		
		self.Comments = []
		

	def toxml(self):
		element = ElementTree.Element('Post')
		
		ElementTree.SubElement(element,'Content').text = self.Content
		
		ElementTree.SubElement(element,'Permalink').text = self.Permalink
		
		ElementTree.SubElement(element,'Author').text = self.Author
		
		ElementTree.SubElement(element,'AuthorLink').text = self.AuthorLink
		
		ElementTree.SubElement(element,'Title').text = self.Title
		
		ElementTree.SubElement(element,'Published').text = self.Published.isoformat()
		

		
		Tagselement = ElementTree.Element('Tags')
		for i in self.Tags:		
			ElementTree.SubElement(Tagselement,'item').text = i
		element.append(Tagselement)
		
		Commentselement = ElementTree.Element('Comments')
		for i in self.Comments:		
			Commentselement.append(i.toxml())
		element.append(Commentselement)
		
		
		return element

class Comment:
	def __init__(self):
		
		self.Content = u''
		
		self.Permalink = u''
		
		self.Author = u''
		
		self.AuthorLink = u''
		
		self.Title = u''
		
		self.Published = datetime(1970,1,1)
		

		

	def toxml(self):
		element = ElementTree.Element('Comment')
		
		ElementTree.SubElement(element,'Content').text = self.Content
		
		ElementTree.SubElement(element,'Permalink').text = self.Permalink
		
		ElementTree.SubElement(element,'Author').text = self.Author
		
		ElementTree.SubElement(element,'AuthorLink').text = self.AuthorLink
		
		ElementTree.SubElement(element,'Title').text = self.Title
		
		ElementTree.SubElement(element,'Published').text = self.Published.isoformat()
		

		
		
		return element



