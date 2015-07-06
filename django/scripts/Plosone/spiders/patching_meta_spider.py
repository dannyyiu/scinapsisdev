import scrapy
from datetime import datetime
from scrapy.spider import BaseSpider
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from Plosone.items import pubMetaItem, pubMNMItem, pubResultItem, pubFigureItem, pubSIItem
from scin.models import pub_meta

class PlosonePatchSpider(CrawlSpider):
    name = "PlosoneMetaPatch"
    allowed_domains = ["plosone.com", "plosone.org", "plos.org"]
    doc_id = 0
	
    def __init__(self, *args, **kwargs): 
      super(PlosonePatchSpider, self).__init__(*args, **kwargs) 
      self.start_urls = [kwargs.get('start_url')] 
      self.doc_id = int(kwargs.get('doc_id'))
	
    def parse(self, response):
		doc_instance = pub_meta.objects.get(id=self.doc_id)
		
		# find articleInfo
		infoList = response.xpath("//div[@class='articleinfo']/p")
		for infoContent in infoList:
			content = infoContent.xpath("string()").re(r"(?<=Citation: ).*")
			if len(content) > 0:
				citation = content
		
		if len(citation) > 0:
			doc_instance.citation = citation[0]
			doc_instance.save()
		