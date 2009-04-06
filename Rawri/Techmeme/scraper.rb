require 'hpricot'
require 'activerecord'
require 'open-uri'

ActiveRecord::Base.establish_connection(
	:adapter	=>	"mysql",
	:host		=>	"localhost",
	:username	=>	"root",
	:password	=>	"plasmafury",
	:database	=>	"techmeme"
)

class Story < ActiveRecord::Base
end

def parse_cite(cite)
	if (cite.inner_html =~ /\s\/\s/) == nil
		#There is no /, means we have only an Author name or site name
		#The cite can either be an Author Name or Site Name
		#So I just assume the link is to site, and name is Author
		#Since I don't have a proper site_name, site_url = site_name
		site_url = cite.at('a')['HREF']
		site_name = site_url
		author = cite.at('a').inner_html
	else
		#We have both an Author and a Site folks
		site_url = cite.at('a')['HREF']
		site_name = cite.at('a').inner_html
		cite.inner_html =~ /([^\/]+)\//
		author = $1
	end
	return site_url, site_name, author
end

def story_from_lnkr(lnkr)
	site_url, site_name, author = parse_cite(lnkr.at('cite'))
	return Story.new(
		:url => (lnkr/'a').last['HREF'],
		:title => (lnkr/'a').last.inner_html,
		:site_url => site_url,
		:site_name => site_name,
		:author => author)
end

def story_from_heditem(heditem)
#	if heditem.at("strong") == nil
		#nils out the stuff in the New Item Finder thingy :)
#		return nil
#	end
	site_url, site_name, author = parse_cite(heditem.at('cite'))
	story = Story.new(		
		:url => (heditem/"strong/a").first['HREF'],
		:title => (heditem/"strong/a").first.inner_html,
		:permalink => (heditem/"a[@TITLE='Permalink']").first["HREF"]
	)

	return story
end

def story_from_item(item)
	site_url, site_name, author = parse_cite(item.at('cite'))

	story = Story.new(
		:url => (item/"div[@CLASS='ii']/strong/a").first['HREF'],
		:title => (item/"div[@CLASS='ii']/strong/a").first.inner_html,
		:permalink => (item/"a[@TITLE='Permalink']").first["HREF"]
	)
	
	puts story		
end


def stories_from_page(uri)
	page = Hpricot(open(uri))
	items = page/"//div[@CLASS='clus']//div[@CLASS='item']"
	heditems = page/"//div[@CLASS='relitems']//div[@CLASS='heditem']"

	heditems.each do |item|
		story_from_heditem(item)
		(item/"div[@CLASS='lnkr']").each do |lnkr|
			if lnkr.at('cite') != nil
				l = story_from_lnkr(lnkr)
				puts "\t" + l.url
			end

		end
	end
end

stories_from_page('http://techmeme.com')

