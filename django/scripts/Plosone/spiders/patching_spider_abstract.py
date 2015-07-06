import scrapy
from datetime import datetime
from scrapy.spider import BaseSpider
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from Plosone.items import pubMetaItem, pubMNMItem, pubResultItem, pubFigureItem, pubSIItem, pubAbstractItem, pubDiscussionItem
from scin.models import pub_meta

class PlosonePatchSpider(CrawlSpider):
    name = "PlosonePatchAbstract"
    allowed_domains = ["plosone.com", "plosone.org", "plos.org"]
    doc_id = 0
	
    def __init__(self, *args, **kwargs): 
      super(PlosonePatchSpider, self).__init__(*args, **kwargs) 
      self.start_urls = [kwargs.get('start_url')] 
      self.doc_id = int(kwargs.get('doc_id'))
	
    def parse(self, response):
		# define instance
		doc_instance = pub_meta.objects.get(id=self.doc_id)
	
		# STEP1: patch abstract
		absSelectorStr = "//div[contains(@class,'abstract')]"
		absSelector = response.xpath(absSelectorStr)
		
		absHeaderListStr = "//div[contains(@class,'abstract')]/h3/text()"
		absHeaderList = absSelector.xpath(absHeaderListStr).extract()
		if len(absHeaderList) > 0:
			headerSeq = 1
			for subHeader in absHeaderList:
				#subHeaderStr = "//h4[%d]" % headerSeq
				subHeaderStr = "//div[contains(@class,'abstract')]/h3[%d]" % (headerSeq)
				for h4 in absSelector.xpath(subHeaderStr):
					paragraphs = h4.xpath("""set:difference(./following-sibling::p,
													./following-sibling::h3[1]/following-sibling::p)""").extract()
					contentSeq = 1
					for prgrph in paragraphs:
						item = pubAbstractItem()
						item['doc'] = doc_instance
						item['section_id'] = headerSeq
						item['header'] = subHeader
						item['content_seq'] = contentSeq
						item['content'] = prgrph
						item.save()
						contentSeq = contentSeq + 1
				headerSeq = headerSeq + 1
		else:
			paragraphs = absSelector.xpath("p")
			contentSeq = 1
			for prgrph in paragraphs:
				item = pubAbstractItem()
				item['doc'] = doc_instance
				item['section_id'] = 1
				item['header'] = ""
				item['content_seq'] = contentSeq
				content = prgrph.xpath("string()").extract()
				if len(content) > 0:
					item['content'] = content[0]
				item.save()
				contentSeq = contentSeq + 1
		
		# STEP2: patch discussion
		headerList = response.xpath("//div[contains(@id,'section')]/h2/text()").extract()		# WARNING: content structure changed

		# find section id having title "Discussion"
		count = 0
		disHeaderNb = 0
		for header in headerList:
			if header == "Discussion":
				disHeaderNb = count
				break
			count = count + 1

		# assign disucssion section selector
		disSelectorStr = "//div[@id='section%d']" % disHeaderNb
		disSelector = response.xpath(disSelectorStr)

		disHeaderListStr = "//div[@id='section%d']/h3/text()" % disHeaderNb
		disHeaderList = disSelector.xpath(disHeaderListStr).extract()
		if len(disHeaderList) > 0:
			headerSeq = 1
			for subHeader in disHeaderList:
				#subHeaderStr = "//h4[%d]" % headerSeq
				subHeaderStr = "//div[@id='section%d']/h3[%d]" % (disHeaderNb, headerSeq)
				for h4 in disSelector.xpath(subHeaderStr):
					paragraphs = h4.xpath("""set:difference(./following-sibling::p,
													./following-sibling::h3[1]/following-sibling::p)""").extract()
					contentSeq = 1
					for prgrph in paragraphs:
						item = pubDiscussionItem()
						item['doc'] = doc_instance
						item['section_id'] = headerSeq
						item['header'] = subHeader
						item['content_seq'] = contentSeq
						item['content'] = prgrph
						item.save()
						contentSeq = contentSeq + 1
				headerSeq = headerSeq + 1
		else:
			paragraphs = disSelector.xpath("p")
			contentSeq = 1
			for prgrph in paragraphs:
				item = pubDiscussionItem()
				item['doc'] = doc_instance
				item['section_id'] = 1
				item['header'] = ""
				item['content_seq'] = contentSeq
				content = prgrph.xpath("string()").extract()
				if len(content) > 0:
					item['content'] = content[0]
				item.save()
				contentSeq = contentSeq + 1
				