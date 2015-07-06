import sys
import MySQLdb
import codecs
from warnings import filterwarnings

def search_tech(doc_id):
	filterwarnings('ignore', category = MySQLdb.Warning)
	sys.stdout = codecs.getwriter('utf8')(sys.stdout)
	try:
		mysql = MySQLdb.connect(user='root',passwd='password1',db='scin_db',host='127.0.0.1',port=3306, autocommit = 'True', charset = 'utf8', use_unicode = True)
		mysql_cursor = mysql.cursor()
		
		# call search technique keywords
		args = [doc_id]
		mysql_cursor.callproc( 'scin_db.pub_technique_exists', args )

		query = ("SELECT count(1) as count FROM scin_db.pub_technique_result WHERE doc_id = %s ")
		mysql_cursor.execute(query, (doc_id,))

		for (count) in mysql_cursor:
		  countStr = "count: %d " %count
		  #print countStr

		mysql_cursor.close()
		mysql.close()
		
		return count[0]

	except MySQLdb.Error, e:
		errmsg = "MySQL Error @run_technique (@%d) %d:  %s" % ( doc_id, e.args[0], e.args[1] )
		with open("error.log", 'w') as w:
			w.write(errmsg)
		sys.exit(1)
