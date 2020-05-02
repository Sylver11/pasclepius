from dotenv import load_dotenv
import pandas as pd
import os

def setupTable():
    sql_drop_table = "DROP TABLE treatments"
    sql_drop_table_invoice = "DROP TABLE andrea_invoice"
    sql_create_table = """CREATE TABLE treatments (
        id int(11) NOT NULL AUTO_INCREMENT,
        item int(11) NOT NULL,
        description LONGTEXT COLLATE utf8_bin NOT NULL,
        units int(11) NOT NULL,
        value decimal(10,2) NOT NULL,
        category varchar(255) COLLATE utf8_bin NOT NULL,
        tariff varchar(255) NOT NULL,
        PRIMARY KEY (id)
        )AUTO_INCREMENT=1 ;"""
  # ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin

    sql_create_table_invoice = """CREATE TABLE andrea_invoice (
        id int(11) NOT NULL AUTO_INCREMENT,
        name varchar(255) NOT NULL,
        date DATETIME NOT NULL,
        medical varchar(255) NOT NULL,
        invoice varchar(255) NOT NULL,
        url varchar(255) NOT NULL,
        treatments varchar(255) NOT NULL,
        dates varchar(255) NOT NULL,
        tariff varchar(255) NOT NULL,
        main varchar(255),
        dob varchar(255),
        number varchar(255),
        `case`varchar(255),
        po int(11),
        PRIMARY KEY (id))
        AUTO_INCREMENT=1 ;"""

#
        #ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin
    conn = pool.connection()
    cursor = conn.cursor()
    cursor.execute(sql_drop_table)
    cursor.execute(sql_drop_table_invoice)
    cursor.execute(sql_create_table)
    cursor.execute(sql_create_table_invoice)
    data = pd.read_csv (os.getenv("SYSTEM_URL") + '/Documents/treatments.csv', delimiter=';')
    df = pd.DataFrame(data, columns= ['item','description','units','value','category', 'tariff'])
    sql_insert =  """INSERT INTO treatments (item, description, units, value,category, tariff)  VALUES(%s,%s,%s,%s,%s,%s)"""
    for row in df.itertuples():
        value = row.item, row.description, row.units, row.value, row.category, row.tariff
        cursor.execute(sql_insert, value)
    cursor.close()
    conn.close()

if __name__ == '__main__':
    load_dotenv()
    from db_utils import pool
    setupTable()

#mysqlimport --ignore-lines=1 --fields-terminated-by=\; --columns='item,description,units,value,category,tariff' --local -u root -p pasclepius /Users/justusvoigt/Documents/treatments.csv
