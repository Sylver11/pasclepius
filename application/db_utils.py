import pymysql
from DBUtils.PooledDB import PooledDB
import os


pool = PooledDB(creator = pymysql,
                               host= 'localhost',
                               user= os.getenv("DATABASE_USER"),
                               password= os.getenv("DATABASE_PASSWORD"),
                               database= os.getenv("DATABASE_NAME"),
                               autocommit=True,
                               charset='utf8mb4',
                               cursorclass=pymysql.cursors.DictCursor,
                               blocking=False,
                               maxconnections=10)

