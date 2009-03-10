

from datetime import datetime
from xml.etree import ElementTree
import sqlite3
import os

class FriendFeedUsers:

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



class User:
	def __init__(self):
		
		self.Name = u''
		
		self.TotalComments = 0
		
		self.ID = u''
		
		self.TotalLikes = 0
		
		self.LastWeekLikes = 0
		
		self.NickName = u''
		
		self.LastWeekComments = 0
		
		self.ProfileURL = u''
		

		
		self.Subscriptions = []
		
		self.Services = []
		
		self.Rooms = []
		

	def toxml(self):
		element = ElementTree.Element('User')
		
		ElementTree.SubElement(element,'Name').text = self.Name
		
		ElementTree.SubElement(element,'TotalComments').text = str(self.TotalComments)
		
		ElementTree.SubElement(element,'ID').text = self.ID
		
		ElementTree.SubElement(element,'TotalLikes').text = str(self.TotalLikes)
		
		ElementTree.SubElement(element,'LastWeekLikes').text = str(self.LastWeekLikes)
		
		ElementTree.SubElement(element,'NickName').text = self.NickName
		
		ElementTree.SubElement(element,'LastWeekComments').text = str(self.LastWeekComments)
		
		ElementTree.SubElement(element,'ProfileURL').text = self.ProfileURL
		

		
		Subscriptionselement = ElementTree.Element('Subscriptions')
		for i in self.Subscriptions:		
			Subscriptionselement.append(i.toxml())
		element.append(Subscriptionselement)
		
		Serviceselement = ElementTree.Element('Services')
		for i in self.Services:		
			Serviceselement.append(i.toxml())
		element.append(Serviceselement)
		
		Roomselement = ElementTree.Element('Rooms')
		for i in self.Rooms:		
			Roomselement.append(i.toxml())
		element.append(Roomselement)
		
		
		return element

class Subscription:
	def __init__(self):
		
		self.Name = u''
		
		self.ID = u''
		
		self.NickName = u''
		
		self.ProfileURL = u''
		

		

	def toxml(self):
		element = ElementTree.Element('Subscription')
		
		ElementTree.SubElement(element,'Name').text = self.Name
		
		ElementTree.SubElement(element,'ID').text = self.ID
		
		ElementTree.SubElement(element,'NickName').text = self.NickName
		
		ElementTree.SubElement(element,'ProfileURL').text = self.ProfileURL
		

		
		
		return element

class Room:
	def __init__(self):
		
		self.Name = u''
		
		self.URL = u''
		
		self.ID = u''
		
		self.NickName = u''
		

		

	def toxml(self):
		element = ElementTree.Element('Room')
		
		ElementTree.SubElement(element,'Name').text = self.Name
		
		ElementTree.SubElement(element,'URL').text = self.URL
		
		ElementTree.SubElement(element,'ID').text = self.ID
		
		ElementTree.SubElement(element,'NickName').text = self.NickName
		

		
		
		return element

class Service:
	def __init__(self):
		
		self.IconURL = u''
		
		self.Name = u''
		
		self.ID = u''
		
		self.ProfileURL = u''
		

		

	def toxml(self):
		element = ElementTree.Element('Service')
		
		ElementTree.SubElement(element,'IconURL').text = self.IconURL
		
		ElementTree.SubElement(element,'Name').text = self.Name
		
		ElementTree.SubElement(element,'ID').text = self.ID
		
		ElementTree.SubElement(element,'ProfileURL').text = self.ProfileURL
		

		
		
		return element



