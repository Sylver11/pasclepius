from dotenv import load_dotenv
import pandas as pd
import os

def setupTable():
    sql_drop_table = "DROP TABLE treatments"
    sql_drop_table_invoice = "DROP TABLE invoices"
    sql_drop_table_users = "DROP TABLE users"
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

    sql_create_table_invoice = """CREATE TABLE invoices (
        id MEDIUMINT NOT NULL AUTO_INCREMENT,
        uuid_text varchar(36) NOT NULL,
        name varchar(255) NOT NULL,
        date_created DATETIME NOT NULL,
        date_invoice DATETIME NOT NULL,
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
        submitted_on DATETIME,
        paid BOOLEAN NOT NULL DEFAULT false,
        balance int(11),
        remind_me DATETIME,
        PRIMARY KEY (id));"""

    sql_create_table_users = """CREATE TABLE users (
        id MEDIUMINT NOT NULL AUTO_INCREMENT,
        uuid_bin binary(16),
        uuid_text varchar(36) generated always as
            (insert(
                insert(
                    insert(
                        insert(hex(uuid_bin),9,0,'-'),
                        14,0,'-'),
                    19,0,'-'),
                24,0,'-')
            ) virtual,
        title varchar(255) NOT NULL,
        name varchar(255) NOT NULL,
        email varchar(100) NOT NULL,
        password varchar(255) NOT NULL,
        phone varchar(255),
        cell varchar(255) NOT NULL,
        fax varchar(255),
        pob varchar(255) NOT NULL,
        city varchar(255) NOT NULL,
        country varchar(255) NOT NULL,
        bank_holder varchar(255) NOT NULL,
        bank_account varchar(255) NOT NULL,
        bank varchar(255) NOT NULL,
        bank_branch varchar(255) NOT NULL,
        practice_number varchar(255) NOT NULL,
        practice_name varchar(255) NOT NULL,
        hpcna_number varchar(255) NOT NULL,
        qualification varchar(255) NOT NULL,
        specialisation varchar(255),
        premium BOOLEAN NOT NULL DEFAULT false,
        created_on DATETIME NOT NULL DEFAULT NOW(),
        PRIMARY KEY (id));"""


    conn = pool.connection()
    cursor = conn.cursor()
    cursor.execute(sql_drop_table)
    cursor.execute(sql_drop_table_users)
    cursor.execute(sql_drop_table_invoice)
    cursor.execute(sql_create_table)
    cursor.execute(sql_create_table_users)
    cursor.execute(sql_create_table_invoice)
    data = pd.read_csv (os.getenv("CSV_URL"), delimiter=';')
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
