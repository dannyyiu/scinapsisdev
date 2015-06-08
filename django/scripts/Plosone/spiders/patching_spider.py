import scrapy
from datetime import datetime
from scrapy.spider import BaseSpider
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from Plosone.items import pubMetaItem, pubMNMItem, pubResultItem, pubFigureItem, pubSIItem
from scin.models import pub_meta

class PlosonePatchSpider(CrawlSpider):
    name = "PlosonePatch"
    allowed_domains = ["plosone.com", "plosone.org", "plos.org"]
    doc_id = 0
	
    def __init__(self, *args, **kwargs): 
      super(PlosonePatchSpider, self).__init__(*args, **kwargs) 
      self.start_urls = [kwargs.get('start_url')] 
      self.doc_id = int(kwargs.get('doc_id'))
	
    def parse(self, response):
		headerList = response.xpath("//div[contains(@id,'section')]/h2/text()").extract()		# WARNING: content structure changed
		doc_instance = pub_meta.objects.get(id=self.doc_id)
		
		# find section id having title "Supporting Information"
		count = 0
		siHeaderNb = 0
		for header in headerList:
			if header == "Supporting Information":
				siHeaderNb = count
				break
			count = count + 1
		
		# assign supporting information section selector
		resultSelectorStr = "//div[@id='section%d']" % siHeaderNb
		resultSelector = response.xpath(resultSelectorStr)
		
		subHeaderListStr = "//div[@id='section%d']//h3/a/text()" % siHeaderNb
		subHeaderList = resultSelector.xpath(subHeaderListStr).extract()
		
		if len(subHeaderList) > 0:
			headerSeq = 1
			for subHeader in subHeaderList:
				xpathTitleListStr = "//div[@id='section%d']/div[@class='supplementary-material'][%d]/h3/a/text()" % (siHeaderNb, headerSeq)
				xpathUrlListStr = "//div[@id='section%d']/div[@class='supplementary-material'][%d]/h3/a/@href" % (siHeaderNb, headerSeq)
				xpathContentListStr = "//div[@id='section%d']/div[@class='supplementary-material'][%d]/p[@class='preSiDOI']/text()" % (siHeaderNb, headerSeq)
				
				headerList = response.xpath(xpathTitleListStr).extract()
				urlList = response.xpath(xpathUrlListStr).extract()
				contentList = response.xpath(xpathContentListStr).extract()
				
				item = pubSIItem()
				item['doc'] = doc_instance
				item['section_id'] = headerSeq
				if len(headerList) > 0:
					item['header'] = headerList[0]
				if len(urlList) > 0:
					item['url'] = urlList[0]
				if len(contentList) > 0:
					item['content'] = contentList[0]
				item.save()
				headerSeq = headerSeq + 1
		