import sys
import MySQLdb
import codecs

import run_technique
import run_supplier
import run_product
import run_product_tech
import flush_temp_tables

from warnings import filterwarnings

sys.setrecursionlimit(20000)
filterwarnings('ignore', category = MySQLdb.Warning)
sys.stdout = codecs.getwriter('utf8')(sys.stdout)
doc_id = 0
try:
	mysql = MySQLdb.connect(user='root',passwd='password1',db='scin_db',host='127.0.0.1',port=3306, autocommit = 'True', charset = 'utf8', use_unicode = True)
	mysql_cursor = mysql.cursor()
	
	mysql_cursor.execute("select distinct trtab.doc_id as id "
							"from scin_db.pub_technique_result trtab "
							"inner join scin_db.pub_product_result prtab "
							"on trtab.doc_id = prtab.doc_id")
	
	for (id) in mysql_cursor:
		doc_id = id
		print "procesing doc_id: %d" % doc_id
		
		run_product_tech.search_product_tech(doc_id)
		flush_temp_tables.flush_temp_tables(doc_id)
		print "doc_id [%d] search completed" % doc_id
	
	mysql_cursor.close()
	mysql.close()

except MySQLdb.Error, e:
	errmsg = "MySQL Error @tech_prod_only (@%d) %d:  %s" % ( doc_id, e.args[0], e.args[1] )
	with open("error.log", 'w') as w:
		w.write(errmsg)
	sys.exit(1)
