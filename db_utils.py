import pymysql.cursors

# Connect to the database
connection = pymysql.connect(host='localhost',
                             user='root',
                             password='Sylvester12.',
                             db='pasclepius',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)
