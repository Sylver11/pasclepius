from dotenv import load_dotenv
import pandas as pd
import os

def setupTable():
    sql_drop_table_namaf_tariffs = "DROP TABLE namaf_tariffs"
    sql_drop_table_invoice = "DROP TABLE invoices"
    sql_drop_table_users = "DROP TABLE users"
    sql_drop_table_invoice_items = "DROP TABLE invoice_items"

    sql_create_table_namaf_tariffs = """CREATE TABLE namaf_tariffs  (
        id MEDIUMINT NOT NULL AUTO_INCREMENT,
        item int(11) NOT NULL,
        description VARCHAR(500) NOT NULL,
        `procedure` VARCHAR(500),
        units int(11),
        units_specification VARCHAR(255),
        value int(11),
        anaesthetic_units int(11),
        anaesthetic_value int(11),
        category varchar(255),
        sub_category varchar(255),
        sub_sub_category varchar(255),
        sub_sub_sub_category varchar(255),
        note varchar(500),
        tariff varchar(255) NOT NULL,
        PRIMARY KEY (id));"""

    sql_create_table_invoice_items = """CREATE TABLE invoice_items (
        id MEDIUMINT NOT NULL AUTO_INCREMENT,
        uuid_text varchar(36) NOT NULL,
        invoice_id varchar(255) NOT NULL,
        item int(11) NOT NULL,
        units int(11),
        description varchar(500),
        `procedure` VARCHAR(500),
        value int(11),
        date DATETIME NOT NULL,
        note varchar(500),
        modifier int(11),
        status varchar(255),
        PRIMARY KEY (id))"""

    sql_create_table_invoice = """CREATE TABLE invoices (
        id MEDIUMINT NOT NULL AUTO_INCREMENT,
        uuid_text varchar(36) NOT NULL,
        patient_name varchar(255) NOT NULL,
        date_created DATETIME NOT NULL,
        date_invoice DATETIME NOT NULL,
        medical_aid varchar(255) NOT NULL,
        invoice_id varchar(255) NOT NULL,
        invoice_file_url varchar(255) NOT NULL,
        tariff varchar(255) NOT NULL,
        main_member varchar(255),
        patient_birth_date DATETIME,
        medical_number varchar(255),
        case_number varchar(255),
        po_number int(11),
        hospital_name varchar(255),
        admission_date DATETIME,
        discharge_date DATETIME,
        `procedure` varchar(500),
        procedure_date DATETIME,
        diagnosis varchar(500),
        diagnosis_date DATETIME,
        implants varchar(500),
        intra_op varchar(255),
        post_op varchar(255),
        submitted_on DATETIME,
        status varchar(255) NOT NULL DEFAULT 'Not submitted',
        `credit` int(11),
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
        qualification varchar(255),
        specialisation varchar(255),
        premium BOOLEAN NOT NULL DEFAULT false,
        invoice_layout int(11) NOT NULL DEFAULT 1,
        created_on DATETIME NOT NULL DEFAULT NOW(),
        PRIMARY KEY (id));"""


    conn = pool.connection()
    cursor = conn.cursor()
    cursor.execute(sql_drop_table_invoice_items)
    cursor.execute(sql_create_table_invoice_items)
   # cursor.execute(sql_drop_table_users)
    cursor.execute(sql_drop_table_invoice)
    cursor.execute(sql_create_table_invoice)
    cursor.execute(sql_drop_table_namaf_tariffs)
    cursor.execute(sql_create_table_namaf_tariffs)
   # cursor.execute(sql_create_table_users)
    cursor.close()
    conn.close()


def populateTreatment():
    conn = pool.connection()
    cursor = conn.cursor()
    data = pd.read_csv(os.getenv("CSV_URL_NAMAF_TARIFFS"),
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
