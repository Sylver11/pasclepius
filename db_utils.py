import pymysql
from DBUtils.PooledDB import PooledDB
from dotenv import load_dotenv
import os
load_dotenv()


pool = PooledDB(creator = pymysql,
                               host= 'localhost',
                               user= os.getenv("DATABASE_USER"),
                               password= os.getenv("DATABASE_PASSWORD"),
                               database=os.getenv("DATABASE_NAME"),
                               autocommit=True,
                               charset='utf8mb4',
                               cursorclass=pymysql.cursors.DictCursor,
                               blocking=False,
                               maxconnections=10)

