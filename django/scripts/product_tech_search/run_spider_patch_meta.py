import codecs
import MySQLdb
import re
import sys
import os
from warnings import filterwarnings

filterwarnings('ignore', category = MySQLdb.Warning)
sys.stdout = codecs.getwriter('utf8')(sys.stdout)
try:
    mysql = MySQLdb.connect(user='root',passwd='password1',db='scin_db',host='127.0.0.1',port=3306, autocommit = 'True', charset = 'utf8', use_unicode = True)
    mysql_cursor = mysql.cursor()
    
    # call search protein keywords
    query = ("SELECT id, src_address FROM scin_db.scin_pub_meta ORDER BY id")
    mysql_cursor.execute(query)

    for (id, src_address) in mysql_cursor:
		print "PROCESS URL = %s, id = %d " % (src_address, id)
		command = 'scrapy.exe crawl PlosoneMetaPatch -a start_url="%s" -a doc_id="%s"  -s LOG_FILE=patch_output.txt ' % (src_address, id)
		os.system(command)
		print "PROCESS COMPLETE"
	  
except MySQLdb.Error, e:
	errmsg = "MySQL Error (@%d) %d:  %s" % ( doc_id, e.args[0], e.args[1] )
	with open("error.log", 'w') as w:
		w.write(errmsg)
	sys.exit(1)