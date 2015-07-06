# -*- coding: utf-8 -*- 
import codecs
import MySQLdb
import re
import sys
from warnings import filterwarnings


def search_product_tech(doc_id):
	filterwarnings('ignore', category=MySQLdb.Warning)
	sys.stdout = codecs.getwriter('utf8')(sys.stdout)
	try:
		mysql = MySQLdb.connect(user='root', passwd='password1', db='scin_db', host='127.0.0.1', port=3306,
								autocommit='True', charset='utf8', use_unicode=True)
		mysql_cursor = mysql.cursor()

		# call search protein keywords
		args = [doc_id]
		mysql_cursor.callproc('scin_db.pub_technique_product_exists', args)

		query = (
			"SELECT figure_id, si_id, tech_id, technique_group, tech_parental_name, tech_alternative, prod_id, supplier, catalog_nb, prod_name_id, product_name, content FROM scin_db.pub_tech_prod_temp")
		mysql_cursor.execute(query)

		rsltCount = 0
		for (
				figure_id, si_id, tech_id, technique_group, tech_parental_name, tech_alternative, prod_id, supplier, catalog_nb,
				prod_name_id, product_name, content) in mysql_cursor:
			# outputStr = "result: %s, %s, %s, %d, %d " % (tech_parental_name, tech_alternative, product_name, figure_id, si_id)

			# print "process figure#: %d " % figure_id

			# remove "-" from product_name
			product_name_temp = product_name.replace("(", "")
			product_name_temp = product_name.replace(")", "")
			product_name_temp = product_name.replace("-", "")

			sentenceList = re.split(ur'(?<!\w\.\w.)(?<![A-Z]\.)(?<=\.|\?)\s', content)
			for sentence in sentenceList:
				technique_exists = False
				protein_exists = False

				# print "process sentence [%s]" % sentence

				# a. check tech_alternative exists
				pattern = ur'(?i)\b%s\b' % (tech_alternative)
				if re.search(pattern, sentence):
					# print "tech_alternative found [%s]" % tech_alternative
					technique_exists = True
				else:
					continue

				# b. check protein exists:
				wordList = re.split('\s', sentence)

				for word in wordList:
					if len(word) < 3:
						continue

					# remove (, )
					word = word.replace("(", "")
					word = word.replace(")", "")

					# convert greek alphabet
					word = word.replace(u"α", "a")
					word = word.replace(u"β", "b")
					word = word.replace(u"γ", "g")
					word = word.replace(u"δ", "d")
					word = word.replace(u"ε", "e")

					# split words
					subwordList = re.split('-', word)
					subwordList.append(word.replace("-", ""))

					for subword in subwordList:
						if len(subword) < 3:
							continue

						if subword.lower() == product_name_temp.lower():
							# print "product_name_temp found exact match [%s]" % product_name_temp (non-case sensitive )
							protein_exists = True
						elif product_name_temp.lower().startswith(
								subword.lower()) or product_name_temp.lower().endswith(subword.lower()):
							# 2 way search #1
							protein_exists = True
						elif subword.lower().startswith(product_name_temp.lower()) or subword.lower().endswith(
								product_name_temp.lower()):
							# 2 way search #2
							protein_exists = True
						else:
							continue

				if technique_exists and protein_exists:
					rating = getRating(mysql_cursor, sentence, doc_id)
					insertStmt = ("INSERT INTO scin_db.pub_tech_prod_result "
								  "(doc_id, figure_id, si_id, tech_id, technique_group, tech_parental_name, tech_alternative, prod_id, supplier, catalog_nb, prod_name_id, product_name, sentence, rating) "
								  "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)")
					mysql_cursor.execute(insertStmt, (
						doc_id, figure_id, si_id, tech_id, technique_group, tech_parental_name, tech_alternative, prod_id,
						supplier, catalog_nb, prod_name_id, product_name, sentence))
					mysql.commit()

					rsltCount = rsltCount + 1

		mysql_cursor.close()
		mysql.close()

		return rsltCount

	except MySQLdb.Error, e:
		errmsg = "MySQL Error (@%s) %d:  %s" % (doc_id, e.args[0], e.args[1])
		with open("error.log", 'w') as w:
			w.write(errmsg)
		sys.exit(1)


# TODO: 1. review structure technique_result and technique_list related tables
def getRating(mysql_cursor, sentence, doc_id):
	rating = 1
	techParentSet = set()
	productSet = set()

	searchStmt = ("SELECT DISTINCT pn_tab.name as prod_name "
				  "FROM scin_db.pub_product_name pn_tab "
				  "INNER JOIN scin_db.pub_product_result pr_tab "
				  "ON pn_tab.prod_id = pr_tab.prod_id "
				  "WHERE pr_tab.doc_id = %s")
	mysql_cursor.execute(searchStmt, (doc_id))
	for (prod_name) in mysql_cursor:
		productSet.add(prod_name)

	# Rules 1: check sentence with different keyword of different parent (eg.IP + WB)
	searchStmt = (
		"select technique_group, tech_parental_name, tech_alternative from scin_db.pub_technique_result where doc_id = %s")
	mysql_cursor.execute(searchStmt, (doc_id))

	for (technique_group, tech_parental_name, tech_alternative) in mysql_cursor:
		pattern = ur'(?i)\b%s\b' % (tech_alternative)
		if re.search(pattern, sentence):
			techParentSet.add(tech_parental_name)

	if (len(techParentSet) > 1 or len(techParentSet) <= 0):
		rating = 0
		return rating

	# Rule 2: keywords pattern exceptions
	parentTech = list(techParentSet)[0]

	# 2a: a. Immuno-Precipitation or Western Blotting
	if parentTech.lower() == "Immunoprecipitation".lower() or parentTech.lower() == "Western blot".lower():
		rankDownList = ["F/flag", "HA", "H/his", "M/myc", "G/gst", "V5", "B/biotin", "-tagged"]

		for rankDownItem in rankDownList:
			if rankDownItem in sentence:
				# TODO: implement exception
				rating = 0
				return rating

	# 2b: a. Immuno-Staining
	if parentTech.lower() == "Immunofluorescence".lower() or parentTech.lower() == "Immunohistochemistry".lower():
		rankDownList = ["P/phaollodin", "A/annexin V", "P/phase contrast", "H&E", "H/hoechst", "DAPI", "T/tunel",
						"H/haematoxylin", "P/prodpidium iodine", "S/safranin O", "β/Beta/beta-gal/galactosidase"]

		pattern1 = ur'(?i)\b%s\b' % ("stained")
		pattern2 = ur'(?i)\b%s\b' % ("staining")

		containStain = False
		if re.search(pattern1, sentence) or re.search(pattern2, sentence):
			containStain = True

		# 2bi
		for rankDownItem in rankDownList:
			if containStain and rankDownItem in sentence:
				rating = 0
				return rating

		# 2bii
		pattern3 = ur'(?i)\b%s\b' % ("microscopy")
		pattern4 = ur'(?i)\b%s\b' % ("electron")
		if containStain and (re.search(pattern3, sentence) and re.search(pattern4, sentence)):
			rating = 0
			return rating

	# 2c: Western Blotting
	if parentTech.lower() == "Western blot".lower():
		rankDownList = ["S/silver", "C/commassie", "P/ponceau", "S/sypro"]

		for rankDownItem in rankDownList:
			if rankDownItem in sentence:
				rating = 0
				return rating

	# 2d: FACS
	if parentTech.lower() == "FACS".lower():
		rankDownList = ["P/propidium Iodine", "stained", "staining"]

		for rankDownItem in rankDownList:
			if rankDownItem in sentence:
				rating = 0
				return rating

	# 2e: Immuno-Precipitation
	if parentTech.lower() == "Immunoprecipitation".lower():
		pattern1 = ur'(?i)\b%s\b' % ("immunoprecipitation")
		pattern2 = ur'(?i)\b%s\b' % ("chromatin")

		if re.search(pattern1, sentence) and re.search(pattern2, sentence):
			rating = 0
			return rating

	# 2f: Immuno-Staining or Western Blotting
	if parentTech.lower() == "Immunofluorescence".lower() or parentTech.lower() == "Immunohistochemistry".lower() or parentTech.lower() == "Western blot".lower():
		rankDownList = ["Q/quantification", "B/bar graph", "Q/quantified"]

		for rankDownItem in rankDownList:
			if rankDownItem in sentence:
				rating = 0
				return rating

	# 2g: General Rule1
	rankDownListGeneral_1 = ["GFP", "E/eGFP", "RFP", "YFP"]
	for rankDownItem in rankDownListGeneral_1:
		if rankDownItem in sentence:
			rating = 0
			for productItem in productSet:	# reset if keyword exists in product
				rating = 1

		if rating == 0:
			return rating

	# 2h: General Rule2
	rankDownListGeneral_2 = ["siRNA", "shRNA", "K/knock down", "K/knocking down", "RNAi"]
	for rankDownItem in rankDownListGeneral_2:
			if rankDownItem in sentence:
				rating = 0
				return rating

	return rating
