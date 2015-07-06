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
    name = "PlosoneMetaPatch3"
    allowed_domains = ["plosone.com", "plosone.org", "plos.org"]
    doc_id = 0
	
    def __init__(self, *args, **kwargs): 
      super(PlosonePatchSpider, self).__init__(*args, **kwargs) 
      self.start_urls = [kwargs.get('start_url')] 
      self.doc_id = int(kwargs.get('doc_id'))
	
    def parse(self, response):
		doc_instance = pub_meta.objects.get(id=self.doc_id)
		
		# figure list
		pub_figure_list = doc_instance.pub_figure_set.all()
		for doc_figure in pub_figure_list:
			figId = doc_figure.figure_id
			xpathUrlStr = "//div[contains(@class,'figure') and contains(@data-doi,'%s')]/div[contains(@class, 'img-box')]/a/@href" % figId
		
		
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
