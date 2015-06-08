import scrapy
import json
import urllib2
from datetime import datetime
from scrapy.spider import BaseSpider
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from Plosone.items import pubMetaItem, pubMNMItem, pubResultItem, pubFigureItem, pubSIItem
from scin.models import pub_meta

class PlosonePatchSpider(CrawlSpider):
    name = "PlosoneMetaPatch2"
    allowed_domains = ["plosone.com", "plosone.org", "plos.org"]
    doc_id = 0
	
    def __init__(self, *args, **kwargs): 
      super(PlosonePatchSpider, self).__init__(*args, **kwargs) 
      self.start_urls = [kwargs.get('start_url')] 
      self.doc_id = int(kwargs.get('doc_id'))
	
    def parse(self, response):
		doc_instance = pub_meta.objects.get(id=self.doc_id)
		
		# find articleInfo
		poi = doc_instance.doc_id
		source_id = "cited,viewed,saved,discussed"
		print poi

		url = 'http://alm.plos.org:80/api/v5/articles?ids=%s&source_id=%s' % (poi, source_id)

		data = json.load(urllib2.urlopen(url))
		views = data['data'][0]['viewed']
		saves = data['data'][0]['saved']
		shares = data['data'][0]['discussed']
		citation = data['data'][0]['cited']
		print views
		print saves
		print shares
		print citation
		
		# construct author
		author = ""
		authorlist = response.xpath("//div[@class='title-authors']//a[@class='author-name']/text()").extract()

		for authorname in authorlist:
			authorname = authorname.replace("\n", "").strip()
			author = author + authorname
		#print author
		
		# write data
		doc_instance.author = author
		doc_instance.views = views
		doc_instance.saves = saves
		doc_instance.shares = shares
		doc_instance.citation = citation
			
		doc_instance.save()
