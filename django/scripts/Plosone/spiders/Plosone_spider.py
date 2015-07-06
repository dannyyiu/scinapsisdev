import scrapy
import json
import urllib2
from datetime import datetime
from scrapy.spider import BaseSpider
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from Plosone.items import pubMetaItem, pubMNMItem, pubResultItem, pubFigureItem, pubSIItem
from scin.models import pub_meta
from django import db

class PlosoneSpider(CrawlSpider):
    name = "Plosone"
    allowed_domains = ["plosone.com", "plosone.org", "plos.org"]
    start_urls = [
		#'http://www.plosone.org/article/info%3Adoi%2F10.1371%2Fjournal.pone.0061362'		# TODO: input parameter #2
		#'http://www.plosone.org/search/advanced?pageSize=15&sort=&queryField=publication_date&startDateAsString=2013-01-01&endDateAsString=2013-01-10&unformattedQuery=publication_date%3A[2013-01-01T00%3A00%3A00Z+TO+2013-01-10T23%3A59%3A59Z]+&journalOpt=some&filterJournals=PLoSONE&subjectCatOpt=all&filterArticleTypesOpt=all'
		'http://www.plosone.org/search/advanced?searchName=&weekly=&monthly=&startPage=0&pageSize=60&filterKeyword=&resultView=&unformattedQuery=publication_date%3A%5B2012-01-01T00%3A00%3A00Z+TO+2013-01-01T23%3A59%3A59Z%5D&x=0&y=0&sort=Relevance&filterStartDate=&filterEndDate=&filterJournals=PLoSONE'
    ]
    # single page: 'http://www.plosone.org/article/info%3Adoi%2F10.1371%2Fjournal.pone.0061362'
	# single page2: 'http://www.plosone.org/article/info:doi%2F10.1371%2Fjournal.pone.0054089'
    # 20130101 to 20130110: 'http://www.plosone.org/search/advanced?pageSize=15&sort=&queryField=publication_date&startDateAsString=2013-01-01&endDateAsString=2013-01-10&unformattedQuery=publication_date%3A[2013-01-01T00%3A00%3A00Z+TO+2013-01-10T23%3A59%3A59Z]+&journalOpt=some&filterJournals=PLoSONE&subjectCatOpt=all&filterArticleTypesOpt=all'
	# 2012 year: 'http://www.plosone.org/search/advanced?searchName=&weekly=&monthly=&startPage=0&pageSize=60&filterKeyword=&resultView=&unformattedQuery=publication_date%3A%5B2012-01-01T00%3A00%3A00Z+TO+2013-01-01T23%3A59%3A59Z%5D&x=0&y=0&sort=Relevance&filterStartDate=&filterEndDate=&filterJournals=PLoSONE'
    # 2013 year: 'http://www.plosone.org/search/advanced?searchName=&weekly=&monthly=&startPage=0&pageSize=60&filterKeyword=&resultView=&unformattedQuery=publication_date%3A[2013-01-01T00%3A00%3A00Z+TO+2014-01-01T23%3A59%3A59Z]&sort=Relevance&filterStartDate=&filterEndDate=&filterJournals=PLoSONE'
	# 2014 year: 'http://www.plosone.org/search/advanced?searchName=&weekly=&monthly=&startPage=0&pageSize=60&filterKeyword=&resultView=&unformattedQuery=publication_date%3A%5B2014-01-01T00%3A00%3A00Z+TO+2015-01-01T23%3A59%3A59Z%5D&x=7&y=6&sort=Relevance&filterStartDate=&filterEndDate=&filterJournals=PLoSONE'
    
    rules = (
        ###===RULES FOR NEXT PAGE LINK===
        # allow: allows certain link url patterns to be followed.
        # restricted_xpaths: xpath for the next button to follow.
        Rule (SgmlLinkExtractor(allow=(".+", ), ###
              restrict_xpaths=(
              "//div[@class='pagination']/a[@class='next']",) ###
              ), follow=True),
		
        ###===RULES FOR AD PAGE LINK===
        # allow: link patterns for ads to click
        # callback: function name for processing ad page after visiting it
        # restricted_xpaths: xpaths under which the links are located.
        Rule (SgmlLinkExtractor(allow=(".*/article/.+", ), deny=(".*/search/.+"), # ext saccurent
             restrict_xpaths=(
             "//div[@class='main']/ul[@id='search-results']//span[@class='article']/a")
             ),
             callback="parse_item", follow=False),
    )
    counter = 0;
		
    def parse_item(self, response):
		docHeader = self.parseHeader(response)
		self.parseMNM(response, docHeader)
		self.parseResult(response, docHeader)
		self.parseFigure(response, docHeader)
		self.parseSI(response, docHeader)
		
		self.counter += 1;
		url_name = response.url
		db.reset_queries()
		print "[RESULT] scrap paper #%d" % self.counter
		print "[RESULT] url=%s" % url_name
        #documentId = self.parseHeader(response)
        #self.parseMNM(response, documentId)
		
    def parseHeader(self, response):
		publisher = "Plos One"				# TODO: input parameter #1
		src_address = response.url			# self.start_urls[0]
		pdf_address = response.xpath("//div[@class='dload-pdf']//a/@href").extract()
		title = response.xpath("//h1[@id='artTitle']/text()").extract()
				
		doc_id = ""
		editors = ""
		pub_date = ""
		copyright = ""
		data_availibility = ""
		funding = ""
		competing_interest = ""
		citation = ""
		
		infoList = response.xpath("//div[@class='articleinfo']/p")
		for infoContent in infoList:
			content = infoContent.xpath("string()").re(r"(?<=doi:).*")
			if len(content) > 0:
				doc_id = content
			content = infoContent.xpath("string()").re(r"(?<=Editor: ).*\n*.*")
			if len(content) > 0:
				editors = content
			content = infoContent.xpath("string()").re(r"(?<=Published:  )[A-Za-z]+ [0-9]+, [0-9]+")
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
			content = infoContent.xpath("string()").re(r"(?<=Citation: ).*")
			if len(content) > 0:
				citation = content
		
		# author
		author = ""
		authorlist = response.xpath("//div[@class='title-authors']//a[@class='author-name']/text()").extract()

		for authorname in authorlist:
			authorname = authorname.replace("\n", "").strip()
			author = author + authorname
		
		# citations
		poi = doc_id[0]
		source_id = "cited,viewed,saved,discussed"

		url = 'http://alm.plos.org:80/api/v5/articles?ids=%s&source_id=%s' % (poi, source_id)

		data = json.load(urllib2.urlopen(url))
		views = data['data'][0]['viewed']
		saves = data['data'][0]['saved']
		shares = data['data'][0]['discussed']
		citationNum = data['data'][0]['cited']
		
		# update time ad other info
		rec_update_time = datetime.now()
		rec_update_by = "sys"
		
		# debug messages
		#print "publisher = %s" % publisher
		#print "src_address = %s" % src_address
		#print "pdf_address = %s" % pdf_address
		#print "doc_id = %s" % doc_id
		#print "title = %s" % title
		#print "editors = %s" % editors
		#print "pub_date = %s" % pub_date
		#print "copyright = %s" % copyright
		#print "data_availibility = %s" % data_availibility
		#print "funding = %s" % funding
		#print "competing_interest = %s" % competing_interest
        
		# write to database
		item = pubMetaItem()
		item['publisher'] = publisher
		if len(pdf_address) > 0:
			item['pdf_address'] = pdf_address[0]
		item['src_address'] = src_address
		item['doc_id'] = doc_id[0]
		item['title'] = title[0]
		if len(editors) > 0:
			item['editors'] = editors[0]
		if len(pub_date) > 0:
			item['pub_date'] = datetime.strptime(pub_date[0], '%B %d, %Y')			# convert to djan
		if len(copyright) > 0:
			item['copyright'] = copyright[0]
		if len(data_availibility) > 0:
			item['data_availibility'] = data_availibility[0]
		if len(funding) > 0:
			item['funding'] = funding[0]
		if len(competing_interest) > 0:
			item['competing_interest'] = competing_interest[0]
		if len(citation) > 0:
			item['citation'] = citation[0]
		
		item['author'] = author
		item['views'] = views
		item['saves'] = saves
		item['shares'] = shares
		item['citation'] = citationNum
		
		item['rec_update_time'] = datetime.now()			# TODO: use GMT instead
		item['rec_update_by'] = "sys"
		docHeader = item.save()
		
		return docHeader

    def parseMNM(self, response, docHeader):
		headerList = response.xpath("//div[starts-with(@id,'section')]/h2/text()").extract()
		
		# find section id having title "Materials and Methods"
		count = 0
		mnmHeaderNb = 0
		for header in headerList:
			if header == "Materials and Methods" or header == "Methods":
				mnmHeaderNb = count
				break
			count = count + 1
		
		# assign M&M section selector
		mnmSelectorStr = "//div[@id='section%d']" % mnmHeaderNb
		mnmSelector = response.xpath(mnmSelectorStr)
		
		subHeaderListStr = "//div[@id='section%d']/h3/text()" % mnmHeaderNb
		subHeaderList = mnmSelector.xpath(subHeaderListStr).extract()
		if len(subHeaderList) > 0:
			headerSeq = 1
			for subHeader in subHeaderList:
				#subHeaderStr = "//h4[%d]" % headerSeq
				subHeaderStr = "//div[@id='section%d']/h3[%d]" % (mnmHeaderNb, headerSeq)
				for h4 in mnmSelector.xpath(subHeaderStr):
					paragraphs = h4.xpath("""set:difference(./following-sibling::p,
													./following-sibling::h3[1]/following-sibling::p)""").extract()
					contentSeq = 1
					for prgrph in paragraphs:
						item = pubMNMItem()
						item['doc'] = docHeader
						item['section_id'] = headerSeq
						item['header'] = subHeader
						item['content_seq'] = contentSeq
						item['content'] = prgrph
						item.save()
						contentSeq = contentSeq + 1
				headerSeq = headerSeq + 1
		else:
			paragraphs = mnmSelector.xpath("p")
			contentSeq = 1
			for prgrph in paragraphs:
				item = pubMNMItem()
				item['doc'] = docHeader
				item['section_id'] = 1
				item['header'] = ""
				item['content_seq'] = contentSeq
				item['content'] = prgrph.xpath("string()").extract()
				item.save()
				contentSeq = contentSeq + 1
	
    def parseResult(self, response, docHeader):
		headerList = response.xpath("//div[starts-with(@id,'section')]/h2/text()").extract()
		
		# find section id having title "Results"
		count = 0
		resultHeaderNb = 0
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
						item = pubResultItem()
						item['doc'] = docHeader
						item['section_id'] = headerSeq
						item['header'] = subHeader
						item['content_seq'] = contentSeq
						item['content'] = prgrph
						item.save()
						contentSeq = contentSeq + 1
				headerSeq = headerSeq + 1
		else:
			paragraphs = resultSelector.xpath("p")
			contentSeq = 1
			for prgrph in paragraphs:
				item = pubResultItem()
				item['doc'] = docHeader
				item['section_id'] = 1
				item['header'] = ""
				item['content_seq'] = contentSeq
				item['content'] = prgrph.xpath("string()").extract()
				item.save()
				contentSeq = contentSeq + 1
			
    def parseFigure(self, response, docHeader):
		figIdList = response.xpath("//div[contains(@class,'figure')]/@data-doi").extract()
		
		itemId = 0
		for figId in figIdList:
			xpathHeaderStr = "//div[contains(@class,'figure') and contains(@data-doi,'%s')]/div[contains(@class, 'figcaption')]/text()" % figId
			xpathContentStr = "//div[contains(@class,'figure') and contains(@data-doi,'%s')]/p[2]" % figId
			xpathUrlStr = "//div[contains(@class,'figure') and contains(@data-doi,'%s')]/div[contains(@class, 'img-box')]/a/@href" % figId
			
			headerList = response.xpath(xpathHeaderStr).extract()
			contentList = response.xpath(xpathContentStr).extract()
			urlList = response.xpath(xpathUrlStr).extract()
			
			item = pubFigureItem()
			item['doc'] = docHeader
			item['figure_id'] = itemId
			if len(headerList) > 0:
				item['header'] = headerList[0]
			if len(contentList) > 0:
				item['content'] = contentList[0]
			if len(urlList) > 0:
				item['url'] = urlList[0]
			item.save()
			itemId = itemId + 1
				
    def parseSI(self, response, docHeader):
		headerList = response.xpath("//div[contains(@id,'section')]/h2/text()").extract()		# WARNING: content structure changed
		
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
				item['doc'] = docHeader
				item['section_id'] = headerSeq
				if len(headerList) > 0:
					item['header'] = headerList[0]
				if len(urlList) > 0:
					item['url'] = urlList[0]
				if len(contentList) > 0:
					item['content'] = contentList[0]
				item.save()
				headerSeq = headerSeq + 1
		