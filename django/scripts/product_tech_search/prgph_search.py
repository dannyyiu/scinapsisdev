# -*- coding: utf-8 -*-
import codecs
import sys
import re
sys.stdout = codecs.getwriter('utf8')(sys.stdout)

content = "Bar graphs showing the expression of (A) FPR2/ALX mRNA in the rat ipsilateral spinal cord plotted versus time following carrageenan injection to the hind paw, presented as a percent of mRNA levels in control (naive) rat spinal cord. Each bar represents the mean + S.E.M, n= 6-10. * represents a significant difference at p<0.05 as compared with naive spinal cord. FPR2/ALX mRNA is expressed in the rat (B) and human astrocytes (C). GPR32 mRNA is expressed in human astrocytes (C). mRNA levels are expressed as relative units and each bar represents the mean + S.E.M for three repeats. The immunohistochemical images show the expression of FPR2/ALX (D), the astrocyte marker GFAP (E) and the colocalization of FPR2/ALX and GFAP (F) in naive rat lumbar spinal cord."
technique = "immunohistochemical"		# western blotting, western blot, IP
product = "FPR2"

# 1. split sentence
sentenceList = re.split(ur'(?<!\w\.\w.)(?<![A-Z]\.)(?<=\.|\?)\s', content)

for sentence in sentenceList:
	technique_exists = False
	protein_exists = False
	
	print "process sentence [%s]" % sentence

	# a. check technique exists
	#if technique in sentence:
	
	pattern = ur'(?i)\b%s\b' % (technique)
	if re.search(pattern, sentence):
		print "technique found [%s]" % technique
		technique_exists = True
	else:
		continue
		
 
	# b. check protein exists:
	sentence = sentence.replace("(", "")
	sentence = sentence.replace(")", "")
	wordList = re.split('\s|-', sentence)
	
	for word in wordList:
		if len(word) < 3:
			continue

		if word.lower() == product.lower():
			print "product found exact match [%s]" % product
			protein_exists = True
		elif word in product:
			print "product found exact partial match [%s]" % product
			protein_exists = True
		else:
			continue
	

	if technique_exists and protein_exists:
		print "RESULT: [%s] contains technique & product " % sentence
		print "RESULT: technique = %s " % technique
		print "RESULT: product = %s " % product
		# process insert into result

		