from dotenv import load_dotenv
import pandas as pd
import os

def setupTable():
    sql_drop_table_namaf_tariffs = "DROP TABLE namaf_tariffs"
    sql_drop_table_invoice = "DROP TABLE invoices"
    sql_drop_table_users = "DROP TABLE users"


    sql_create_table_namaf_tariffs = """CREATE TABLE namaf_tariffs  (
        id MEDIUMINT NOT NULL AUTO_INCREMENT,
        item int(11) NOT NULL,
        description VARCHAR(500) NOT NULL,
        `procedure` VARCHAR(500),
        units decimal(10,2),
        units_specification VARCHAR(255),
        value decimal(10,2),
        anaesthetic_units decimal(10,2),
        anaesthetic_value decimal(10,2),
        category varchar(255),
        sub_category varchar(255),
        sub_sub_category varchar(255),
        sub_sub_sub_category varchar(255),
        note varchar(255),
        tariff varchar(255) NOT NULL,
        PRIMARY KEY (id));"""


    sql_create_table_invoice = """CREATE TABLE invoices (
        id MEDIUMINT NOT NULL AUTO_INCREMENT,
        uuid_text varchar(36) NOT NULL,
        name varchar(255) NOT NULL,
        date_created DATETIME NOT NULL,
        date_invoice DATETIME NOT NULL,
        medical varchar(255) NOT NULL,
        invoice varchar(255) NOT NULL,
        url varchar(255) NOT NULL,
        modifiers varchar(500),
        `values` varchar(500) NOT NULL,
        treatments varchar(500) NOT NULL,
        dates varchar(500) NOT NULL,
        tariff varchar(255) NOT NULL,
        main varchar(255),
        dob varchar(255),
        number varchar(255),
        `case`varchar(255),
        po int(11),
        hospital varchar(255),
        admission varchar(255),
        discharge varchar(255),
        `procedure` varchar(500),
        procedure_date varchar(255),
        diagnosis varchar(500),
        diagnosis_date varchar(255),
        implants varchar(500),
        intra_op varchar(255),
        post_op varchar(255),
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
        first_name varchar(255) NOT NULL,
        second_name varchar(255) NOT NULL,
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
        invoice_layout int(11) NOT NULL DEFAULT 1,
        created_on DATETIME NOT NULL DEFAULT NOW(),
        PRIMARY KEY (id));"""


    conn = pool.connection()
    cursor = conn.cursor()
   # cursor.execute(sql_drop_table_users)
   # cursor.execute(sql_drop_table_invoice)
    cursor.execute(sql_drop_table_namaf_tariffs)
    cursor.execute(sql_create_table_namaf_tariffs)
   # cursor.execute(sql_create_table_users)
   # cursor.execute(sql_create_table_invoice)

    cursor.close()
    conn.close()


def populateTreatment():
    conn = pool.connection()
    cursor = conn.cursor()

    data = pd.read_csv (os.getenv("CSV_URL_NAMAF_TARIFFS"),
                        delimiter=';', skipinitialspace = True)

    df_namaf_tariffs = pd.DataFrame(data, columns=
                                                 ['item','description',
                                                  'procedure','units',
                                                  'units_specification',
                                                  'value',
                                                  'anaesthetic_units',
                                                  'anaesthetic_value', 'category',
                                                  'sub_category', 'sub_sub_category',
                                                  'sub_sub_sub_category',
                                                  'note', 'tariff'])

    df_namaf_tariffs = df_namaf_tariffs.where(pd.notnull(df_namaf_tariffs), None)

    sql_insert_namaf_tariffs =  """INSERT INTO
    namaf_tariffs (item, description, `procedure`, units,
    units_specification, value, anaesthetic_units,
    anaesthetic_value, category, sub_category, sub_sub_category,
    sub_sub_sub_category, note, tariff)
    VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""

    for row in df_namaf_tariffs.itertuples():
        value = row.item, row.description, row.procedure, row.units, row.units_specification, row.value, row.anaesthetic_units, row.anaesthetic_value, row.category, row.sub_category, row.sub_sub_category, row.sub_sub_sub_category, row.note, row.tariff
        cursor.execute(sql_insert_namaf_tariffs, value)
    cursor.close()
    conn.close()

if __name__ == '__main__':
    load_dotenv()
    from db_utils import pool
    setupTable()
    populateTreatment()