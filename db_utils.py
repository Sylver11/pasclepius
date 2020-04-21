import pymysql
from DBUtils.PooledDB import PooledDB
# Connect to the database
#connection = pymysql.connect(host='localhost',
#                             user='root',
#                             password='Sylvester12.',
#                             db='pasclepius',
#                             charset='utf8mb4',
#                             cursorclass=pymysql.cursors.DictCursor)



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
