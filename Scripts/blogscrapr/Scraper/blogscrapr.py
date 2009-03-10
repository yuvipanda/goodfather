from Blog import Comment, Post, Blog 
from BeautifulSoup import BeautifulSoup
from Controllers import PostsCommentsController, PostsOnlyController
import sys
       
		        
if __name__ == '__main__':
        if sys.argv.count < 3:
                print 'Usage: blogscrapr.py <ScraperScript> <OutputFile>'
                exit()
                	
        scraperName = sys.argv[1]
        outputFilePath = sys.argv[2]
        
        scraper = __import__(scraperName)
        functions = dir(scraper)
                
        blog = Blog(outputFilePath)
        
        if scraper.scraperType == 'PostsComments':
        	controller = PostsCommentsController(scraper)
        elif scraper.scraperType == 'PostsOnly':
        	controller = PostsOnlyController(scraper) 
        
        for p in controller.ExtractPosts():
        	blog.persist(p)
         
