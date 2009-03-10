from Network import SoupFromURL
class PostsCommentsController:
	def PostFromUrl(self,url):
		soup = SoupFromURL(url,usecache=False)
		post = self.scraper.PostFromSoup(soup,url)				
		
		if 'CommentPageURLsFromSoup' in self.functions:
			commentPageURLs = self.scraper.CommentPageURLsFromSoup(soup,url)
			commentLists = [self.scraper.CommentsFromSoup(SoupFromURL(x)) for x in commentPageURLs]
			for commentList in commentLists:
				for comment in commentList:
					post.Comments.append(comment)					
		else:
			post.Comments.append(self.scraper.CommentsFromSoup(soup))						
				
		return post
	
	def ExtractPosts(self):		
		for curPage in self.scraper.PageURLGenerator():            
			self.log("Grabbing page " + curPage)
			curPermalinks = self.scraper.PermalinksFromSoup(SoupFromURL(curPage,usecache=False))            
			if curPermalinks == None:
				break
			
			for pl in curPermalinks:
				post = self.PostFromUrl(pl)
				self.log("Done " + pl)
				yield post
	
	def __init__(self,scraper, logger=None):
		self.scraper = scraper
		self.functions = dir(scraper)
		if logger == None:
			def log(message): print message
			self.log = log
		else:
			self.log = logger
			
class PostsOnlyController:
	def __init__(self, scraper, logger=None):			
		self.scraper = scraper
		if logger == None:
			def log(message): print message
			self.log = log
		else:
			self.log = logger
			
	def ExtractPosts(self):
		for curpage in self.scraper.PageURLGenerator():
			posts = self.scraper.PostsFromPage(SoupFromURL(curpage))
			for p in posts:
				self.log('Done ' + p.title)
				yield p
			
						
			
