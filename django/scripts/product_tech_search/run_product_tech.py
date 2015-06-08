# -*- coding: utf-8 -*- 
import codecs
import MySQLdb
import re
import sys
from warnings import filterwarnings

def search_product_tech(doc_id):
	filterwarnings('ignore', category = MySQLdb.Warning)
	sys.stdout = codecs.getwriter('utf8')(sys.stdout)
	try:
		mysql = MySQLdb.connect(user='root',passwd='password1',db='scin_db',host='127.0.0.1',port=3306, autocommit = 'True', charset = 'utf8', use_unicode = True)
		mysql_cursor = mysql.cursor()
		
		# call search protein keywords
		args = [doc_id]
		mysql_cursor.callproc( 'scin_db.pub_technique_product_exists', args )
		
		query = ("SELECT figure_id, si_id, tech_id, technique_group, tech_parental_name, tech_alternative, prod_id, supplier, catalog_nb, prod_name_id, product_name, content FROM scin_db.pub_tech_prod_temp")
		mysql_cursor.execute(query)
		
		rsltCount = 0
		for (figure_id, si_id, tech_id, technique_group, tech_parental_name, tech_alternative, prod_id, supplier, catalog_nb, prod_name_id, product_name, content) in mysql_cursor:
		  #outputStr = "result: %s, %s, %s, %d, %d " % (tech_parental_name, tech_alternative, product_name, figure_id, si_id)
		  
		  #print "process figure#: %d " % figure_id
		  
		  # remove "-" from product_name
		  product_name_temp = product_name.replace("(","")
		  product_name_temp = product_name.replace(")","")
		  product_name_temp = product_name.replace("-","")
		  
		  sentenceList = re.split(ur'(?<!\w\.\w.)(?<![A-Z]\.)(?<=\.|\?)\s', content)
		  for sentence in sentenceList:
			technique_exists = False
			protein_exists = False
			
			#print "process sentence [%s]" % sentence

			# a. check tech_alternative exists
			pattern = ur'(?i)\b%s\b' % (tech_alternative)
			if re.search(pattern, sentence):
				#print "tech_alternative found [%s]" % tech_alternative
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
				subwordList.append(word.replace("-",""))
				
				for subword in subwordList:
					if len(subword) < 3:
						continue
						
					if subword.lower() == product_name_temp.lower():
						#print "product_name_temp found exact match [%s]" % product_name_temp (non-case sensitive )
						protein_exists = True
					elif product_name_temp.lower().startswith(subword.lower()) or product_name_temp.lower().endswith(subword.lower()):
						# 2 way search #1
						protein_exists = True
					elif subword.lower().startswith(product_name_temp.lower()) or subword.lower().endswith(product_name_temp.lower()):
						# 2 way search #2
						protein_exists = True
					else:
						continue
					
			if technique_exists and protein_exists:
				insertStmt = ("INSERT INTO scin_db.pub_tech_prod_result "
							  "(doc_id, figure_id, si_id, tech_id, technique_group, tech_parental_name, tech_alternative, prod_id, supplier, catalog_nb, prod_name_id, product_name, sentence) "
							  "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)")
				mysql_cursor.execute(insertStmt, (doc_id, figure_id, si_id, tech_id, technique_group, tech_parental_name, tech_alternative, prod_id, supplier, catalog_nb, prod_name_id, product_name, sentence) )
				mysql.commit()
					
				rsltCount = rsltCount + 1

		mysql_cursor.close()
		mysql.close()
		
		return rsltCount

	except MySQLdb.Error, e:
		errmsg = "MySQL Error (@%s) %d:  %s" % ( doc_id, e.args[0], e.args[1] )
		with open("error.log", 'w') as w:
			w.write(errmsg)
		sys.exit(1)
