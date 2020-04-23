import pymysql
from DBUtils.PooledDB import PooledDB
# Connect to the database
# connection = pymysql.connect(host='localhost',
#                             user='root',
#                             password='Sylvester12.',
#                             db='pasclepius',
#                             charset='utf8mb4',
#                             cursorclass=pymysql.cursors.DictCursor)



# you shouldn't ever commit credentials to git
# rather set up environment variables that store these values where ever
# you run the server
pool = PooledDB(creator = pymysql,
                               host= 'localhost',
                               user= 'root',
                               password='Sylvester12.',
                               database='pasclepius',
                               autocommit=True,
                               charset='utf8mb4',
                               cursorclass=pymysql.cursors.DictCursor,
                               blocking=False,
                               maxconnections=10)

#connection = mySQLConnectionPool.connection()

#print(connection)
