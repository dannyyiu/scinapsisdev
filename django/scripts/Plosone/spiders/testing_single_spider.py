import scrapy
from datetime import datetime
from scrapy.spider import BaseSpider
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from Plosone.items import pubMetaItem, pubMNMItem, pubResultItem, pubFigureItem, pubSIItem
from scin.models import pub_meta

class PlosoneSpider(CrawlSpider):
    name = "PlosoneTest"
    allowed_domains = ["plosone.com", "plosone.org", "plos.org"]
    start_urls = [
		'http://journals.plos.org/plosone/article?id=10.1371/journal.pone.0053807'		# TODO: input parameter #2
		#'http://www.plosone.org/search/advanced?pageSize=15&sort=&queryField=publication_date&startDateAsString=2013-01-01&endDateAsString=2013-01-10&unformattedQuery=publication_date%3A[2013-01-01T00%3A00%3A00Z+TO+2013-01-10T23%3A59%3A59Z]+&journalOpt=some&filterJournals=PLoSONE&subjectCatOpt=all&filterArticleTypesOpt=all'
		#'http://www.plosone.org/search/advanced?pageSize=15&sort=&queryField=publication_date&startDateAsString=2013-01-01&endDateAsString=2013-01-10&unformattedQuery=publication_date%3A[2013-01-01T00%3A00%3A00Z+TO+2013-01-10T23%3A59%3A59Z]+&journalOpt=some&filterJournals=PLoSONE&subjectCatOpt=all&filterArticleTypesOpt=all'
    ]
    # single page: 'http://www.plosone.org/article/info%3Adoi%2F10.1371%2Fjournal.pone.0061362'
	# single page2: 'http://www.plosone.org/article/info:doi%2F10.1371%2Fjournal.pone.0054089'
    # 20130101 to 20130110: 'http://www.plosone.org/search/advanced?pageSize=15&sort=&queryField=publication_date&startDateAsString=2013-01-01&endDateAsString=2013-01-10&unformattedQuery=publication_date%3A[2013-01-01T00%3A00%3A00Z+TO+2013-01-10T23%3A59%3A59Z]+&journalOpt=some&filterJournals=PLoSONE&subjectCatOpt=all&filterArticleTypesOpt=all'
    # 2013 year: 'http://www.plosone.org/search/advanced?searchName=&weekly=&monthly=&startPage=0&pageSize=60&filterKeyword=&resultView=&unformattedQuery=publication_date%3A[2013-01-01T00%3A00%3A00Z+TO+2014-01-01T23%3A59%3A59Z]&sort=Relevance&filterStartDate=&filterEndDate=&filterJournals=PLoSONE'
    
    counter = 0;
		
    def parse(self, response):
		#self.parseHeader(response)
		#self.parseMNM(response)
		#self.parseResults(response)
		#self.parseFigure(response)
		self.parseSI(response)
		
		self.counter += 1;
		url_name = response.url
		print "[RESULT] scrap paper #%d" % self.counter
		print "[RESULT] url=%s" % url_name
        #documentId = self.parseHeader(response)
        #self.parseMNM(response, documentId)
		
    def parseHeader(self, response):
		publisher = "Plos One"				# TODO: input parameter #1
		src_address = response.url			# self.start_urls[0]
		pdf_address = response.xpath("//div[@class='download']//a/@href").xpath("string()").extract()
		title = response.xpath("//h1[@id='artTitle']/text()").extract()[0]
				
		doc_id = ""
		editors = ""
		pub_date = ""
		copyright = ""
		data_availibility = ""
		funding = ""
		competing_interest = ""
		
		infoList = response.xpath("//div[@class='articleinfo']/p")
		for infoContent in infoList:
			content = infoContent.xpath("string()").re(r"(?<=doi:).*")
			if len(content) > 0:
				doc_id = content
			content = infoContent.xpath("string()").re(r"(?<=Editor: ).*\n*.*")
			if len(content) > 0:
				editors = content
			content = infoContent.xpath("string()").re(r"(?<=Published: )[A-Za-z]+ [0-9]+, [0-9]+")
			if len(content) > 0:
				pub_date = content
			content = infoContent.xpath("string()").re(r"(?<=Copyright: ).*")
			if len(content) > 0:
				copyright = content
			content = infoContent.xpath("string()").re(r"(?<=Data Availability: ).*")
			if len(content) > 0:
				data_availibility = content
			content = infoContent.xpath("string()").re(r"(?<=Funding: ).*")
			if len(content) > 0:
				funding = content
			content = infoContent.xpath("string()").re(r"(?<=Competing interests: ).*")
			if len(content) > 0:
				competing_interest = content
		
		rec_update_time = datetime.now()
		rec_update_by = "sys"
		
		# debug messages
		print "publisher = %s" % publisher
		print "src_address = %s" % src_address
		print "pdf_address = %s" % pdf_address
		print "doc_id = %s" % doc_id
		print "title = %s" % title
		print "editors = %s" % editors
		print "pub_date = %s" % datetime.strptime(pub_date[0], '%B %d, %Y')
		print "copyright = %s" % copyright
		print "data_availibility = %s" % data_availibility
		print "funding = %s" % funding
		print "competing_interest = %s" % competing_interest
        
		# write to database
		###item = pubMetaItem()
		###item['publisher'] = publisher
		###if len(pdf_address) > 0:
		###	item['pdf_address'] = pdf_address[0]
		###item['src_address'] = src_address
		###item['doc_id'] = doc_id[0]
		###item['title'] = title[0]
		###if len(editors) > 0:
		###	item['editors'] = editors[0]
		###if len(pub_date) > 0:
		###	item['pub_date'] = datetime.strptime(pub_date[0], '%B %d, %Y')			# convert to djan
		###if len(copyright) > 0:
		###	item['copyright'] = copyright[0]
		###if len(data_availibility) > 0:
		###	item['data_availibility'] = data_availibility[0]
		###if len(funding) > 0:
		###	item['funding'] = funding[0]
		###if len(competing_interest) > 0:
		###	item['competing_interest'] = competing_interest[0]
		###item['rec_update_time'] = datetime.now()			# TODO: use GMT instead
		###item['rec_update_by'] = "sys"
		###docHeader = item.save()

    def parseMNM(self, response):
		headerList = response.xpath("//div[starts-with(@id,'section')]/h2/text()").extract()			###
		
		# find section id having title "Materials and Methods"
		count = 1																						###
		for header in headerList:
			if header == "Materials and Methods" or header == "Methods":
				mnmHeaderNb = count
				break
			count = count + 1
			
		print "MNM seciont id = %s " % mnmHeaderNb
		
		# assign M&M section selector
		mnmSelectorStr = "//div[@id='section%d']" % mnmHeaderNb
		mnmSelector = response.xpath(mnmSelectorStr)
		
		subHeaderListStr = "//div[@id='section%d']/h3/text()" % mnmHeaderNb							###
		subHeaderList = mnmSelector.xpath(subHeaderListStr).extract()
		if len(subHeaderList) > 0:
			headerSeq = 1
			for subHeader in subHeaderList:
				#subHeaderStr = "//h4[%d]" % headerSeq
				subHeaderStr = "//div[@id='section%d']/h3[%d]" % (mnmHeaderNb, headerSeq)			###
				for h4 in mnmSelector.xpath(subHeaderStr):
					paragraphs = h4.xpath("""set:difference(./following-sibling::p,
													./following-sibling::h3[1]/following-sibling::p)""").extract()			###
					contentSeq = 1
					for prgrph in paragraphs:
						print "section_id = %s" % headerSeq
						print "header = %s" % subHeader
						print "content_seq = %s" % contentSeq
						try:
							print "content = %s" % prgrph
						except:
							print "content error in decoding"
						#item = pubMNMItem()
						#item['doc_id'] = docHeader
						#item['section_id'] = headerSeq
						#item['header'] = subHeader
						#item['content_seq'] = contentSeq
						#item['content'] = prgrph
						#item.save()
						contentSeq = contentSeq + 1
				headerSeq = headerSeq + 1
		else:
			paragraphs = mnmSelector.xpath("p")
			contentSeq = 1
			for prgrph in paragraphs:
				print "section_id = %s" % "1"
				print "header = %s" % ""
				print "content_seq = %s" % contentSeq
				try:
					print "content = %s" % prgrph.xpath("string()").extract()
				except:
					print "content error in decoding"
				#item = pubMNMItem()
				#item['doc_id'] = docHeader
				#item['section_id'] = 1
				#item['header'] = ""
				#item['content_seq'] = contentSeq
				#item['content'] = prgrph.xpath("string()").extract()
				#item.save()
				contentSeq = contentSeq + 1
				
    def parseResults(self, response):
		headerList = response.xpath("//div[starts-with(@id,'section')]/h2/text()").extract()
		
		# find section id having title "Results"
		count = 1
		for header in headerList:
			if header == "Results":
				resultHeaderNb = count
				break
			count = count + 1
		
		# assign M&M section selector
		resultSelectorStr = "//div[@id='section%d']" % resultHeaderNb
		resultSelector = response.xpath(resultSelectorStr)
		
		subHeaderListStr = "//div[@id='section%d']/h3/text()" % resultHeaderNb
		subHeaderList = resultSelector.xpath(subHeaderListStr).extract()
		if len(subHeaderList) > 0:
			headerSeq = 1
			for subHeader in subHeaderList:
				#subHeaderStr = "//h4[%d]" % headerSeq
				subHeaderStr = "//div[@id='section%d']/h3[%d]" % (resultHeaderNb, headerSeq)
				for h4 in resultSelector.xpath(subHeaderStr):
					paragraphs = h4.xpath("""set:difference(./following-sibling::p,
													./following-sibling::h3[1]/following-sibling::p)""").extract()
					contentSeq = 1
					for prgrph in paragraphs:
						print "section_id = %s" % headerSeq
						print "header = %s" % subHeader
						print "content_seq = %s" % contentSeq
						try:
							print "content = %s" % prgrph
						except:
							print "content error in decoding"
						#item = pubResultItem()
						#item['doc_id'] = docHeader
						#item['section_id'] = headerSeq
						#item['header'] = subHeader
						#item['content_seq'] = contentSeq
						#item['content'] = prgrph
						#item.save()
						contentSeq = contentSeq + 1
				headerSeq = headerSeq + 1
		else:
			paragraphs = resultSelector.xpath("p")
			contentSeq = 1
			for prgrph in paragraphs:
				print "section_id = %s" % "1"
				print "header = %s" % ""
				print "content_seq = %s" % contentSeq
				try:
					print "content = %s" % prgrph.xpath("string()").extract()
				except:
					print "content error in decoding"
				#item = pubResultItem()
				#item['doc_id'] = docHeader
				#item['section_id'] = 1
				#item['header'] = ""
				#item['content_seq'] = contentSeq
				#item['content'] = prgrph.xpath("string()").extract()
				#item.save()
				contentSeq = contentSeq + 1
	
    def parseFigure(self, response):
		figIdList = response.xpath("//div[contains(@class,'figure')]/@data-doi").extract()
		
		itemId = 1
		for figId in figIdList:
			xpathHeaderStr = "//div[contains(@class,'figure') and contains(@data-doi,'%s')]/div[contains(@class, 'figcaption')]/text()" % figId
			xpathContentStr = "//div[contains(@class,'figure') and contains(@data-doi,'%s')]/p[2]" % figId
			xpathUrlStr = "//div[contains(@class,'figure') and contains(@data-doi,'%s')]/div[contains(@class, 'img-box')]/a/@href" % figId
			
			headerList = response.xpath(xpathHeaderStr).extract()
			contentList = response.xpath(xpathContentStr).extract()
			urlList = response.xpath(xpathUrlStr).extract()
			
			if len(headerList) > 0:
				print "header = %s " % headerList[0]
			if len(contentList) > 0:
				try:
					print "content = %s " % contentList[0]
				except:
					print "content encoding problem"
			if len(urlList) > 0:
				print "url = %s " % urlList[0]
			itemId = 1
	
    def parseSI(self, response):
		headerList = response.xpath("//div[contains(@id,'section')]/h2/text()").extract()		# WARNING: content structure changed
		
		# find section id having title "Supporting Information"
		count = 0
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
				item['doc_id'] = pub_meta.objects.get(id=2)
				item['section_id'] = headerSeq
				if len(headerList) > 0:
					item['header'] = headerList[0]
				if len(urlList) > 0:
					item['url'] = urlList[0]
				if len(contentList) > 0:
					item['content'] = contentList[0]
				item.save()
				headerSeq = headerSeq + 1
				
	