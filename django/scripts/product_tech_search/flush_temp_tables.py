import sys
import MySQLdb
import codecs
from warnings import filterwarnings

def flush_temp_tables(doc_id):
	filterwarnings('ignore', category = MySQLdb.Warning)
	sys.stdout = codecs.getwriter('utf8')(sys.stdout)
	try:
		mysql = MySQLdb.connect(user='root',passwd='password1',db='scin_db',host='127.0.0.1',port=3306, autocommit = 'True', charset = 'utf8', use_unicode = True)
		mysql_cursor = mysql.cursor()
		
		# call search protein keywords
		args = [doc_id]
		mysql_cursor.callproc( 'scin_db.pub_flush_temp_tables', args )

		mysql_cursor.close()
		mysql.close()

	except MySQLdb.Error, e:
		errmsg = "MySQL Error @flust_temp_table (@%d) %d:  %s" % ( doc_id, e.args[0], e.args[1] )
		with open("error.log", 'w') as w:
			w.write(errmsg)
		sys.exit(1)