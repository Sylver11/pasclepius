import os
import pandas as pd
from dotenv import load_dotenv

load_dotenv()

def setupTable():
    sql_drop_table_namaf_tariffs = "DROP TABLE namaf_tariffs"
    sql_drop_table_invoice = "DROP TABLE invoices"
    sql_drop_table_users = "DROP TABLE users"
    sql_drop_table_invoice_items = "DROP TABLE invoice_items"
    sql_drop_table_user_workbench = "DROP TABLE user_workbench"
    sql_drop_table_patients = "DROP TABLE patients"

    sql_create_table_namaf_tariffs = """CREATE TABLE namaf_tariffs  (
        id MEDIUMINT NOT NULL AUTO_INCREMENT,
        item int(11) NOT NULL,
        description VARCHAR(500) NOT NULL,
        `procedure` VARCHAR(500),
        units int(11),
        units_specification VARCHAR(255),
        value_cent int(11),
        anaesthetic_units int(11),
        anaesthetic_value_cent int(11),
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
        value_cent int(11),
        post_value_cent int(11),
        date DATE NOT NULL,
        note varchar(500),
        modifier int(11),
        status varchar(255),
        PRIMARY KEY (id))"""

    sql_create_table_invoice = """CREATE TABLE invoices (
        id MEDIUMINT NOT NULL AUTO_INCREMENT,
        uuid_text varchar(36) NOT NULL,
        patient_name varchar(255) NOT NULL,
        date_created DATETIME NOT NULL DEFAULT NOW(),
        date_invoice DATE NOT NULL,
        medical_aid varchar(255) NOT NULL,
        invoice_id varchar(255) NOT NULL,
        invoice_file_url varchar(255) NOT NULL,
        tariff varchar(255) NOT NULL,
        main_member varchar(255),
        patient_birth_date DATE,
        medical_number varchar(255),
        case_number varchar(255),
        po_number int(11),
        hospital_name varchar(255),
        admission_date DATE,
        discharge_date DATE,
        `procedure` varchar(500),
        procedure_date DATE NULL,
        diagnosis varchar(500),
        diagnosis_date DATE NULL,
        implants varchar(500),
        intra_op varchar(255),
        post_op varchar(255),
        submitted_on DATE,
        invoice_layout int(11),
        status varchar(255) NOT NULL DEFAULT 'not-submitted',
        credit_cent int(11) NOT NULL DEFAULT 0,
        remind_me DATETIME,
        PRIMARY KEY (id));"""


    sql_create_table_patients = """ CREATE TABLE patients (
        id int(11) NOT NULL AUTO_INCREMENT,
        uuid_text varchar(36) NOT NULL,
        patient_name varchar(255) NOT NULL,
        medical_aid varchar(255) NOT NULL,
        main_member varchar(255),
        patient_birth_date DATE NULL,
        medical_number varchar(255),
        case_number varchar(255),
        patient_note varchar(500),
        created_on DATETIME NOT NULL DEFAULT NOW(),
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

    sql_create_table_user_workbench = """CREATE TABLE user_workbench (
    uuid_text VARCHAR(36) NOT NULL,
    work_type VARCHAR(255) NOT NULL,
    work_quality TEXT NOT NULL,
    created_on DATETIME NOT NULL DEFAULT NOW());"""

    create_trigger_status = """CREATE TRIGGER check_settled BEFORE UPDATE ON invoices
    FOR EACH ROW
    BEGIN
    IF NEW.credit_cent = (SELECT SUM(post_value_cent) FROM invoice_items WHERE uuid_text = OLD.uuid_text AND invoice_id = OLD.invoice_id) THEN
    SET NEW.status = 'settled';
    ELSEIF NEW.credit_cent > (SELECT SUM(post_value_cent)
    FROM invoice_items WHERE uuid_text = OLD.uuid_text AND invoice_id =
    OLD.invoice_id) THEN SET NEW.credit_cent = OLD.credit_cent;
    END IF;
    END;"""



    conn = pool.connection()
    cursor = conn.cursor()
    cursor.execute(sql_drop_table_user_workbench)
    cursor.execute(sql_create_table_user_workbench)
    cursor.execute(sql_drop_table_invoice_items)
    cursor.execute(sql_create_table_invoice_items)
    cursor.execute(sql_drop_table_patients)
    cursor.execute(sql_create_table_patients)
    #cursor.execute(sql_drop_table_users)
    cursor.execute(sql_drop_table_invoice)
    cursor.execute(sql_create_table_invoice)
    cursor.execute(sql_drop_table_namaf_tariffs)
    cursor.execute(sql_create_table_namaf_tariffs)
    cursor.execute(create_trigger_status)
    #cursor.execute(sql_create_table_users)
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
                                                  'value_cent',
                                                  'anaesthetic_units',
                                                  'anaesthetic_value_cent', 'category',
                                                  'sub_category', 'sub_sub_category',
                                                  'sub_sub_sub_category',
                                                  'note', 'tariff'])

    df_namaf_tariffs = df_namaf_tariffs.where(pd.notnull(df_namaf_tariffs), None)
    sql_insert_namaf_tariffs =  """INSERT INTO
    namaf_tariffs (item, description, `procedure`, units,
    units_specification, value_cent, anaesthetic_units,
    anaesthetic_value_cent, category, sub_category, sub_sub_category,
    sub_sub_sub_category, note, tariff)
    VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
    for row in df_namaf_tariffs.itertuples():
        value = row.item, row.description, row.procedure, row.units, row.units_specification, row.value_cent, row.anaesthetic_units, row.anaesthetic_value_cent, row.category, row.sub_category, row.sub_sub_category, row.sub_sub_sub_category, row.note, row.tariff
        cursor.execute(sql_insert_namaf_tariffs, value)
    cursor.close()
    conn.close()

if __name__ == '__main__':
    from db_utils import pool
    setupTable()
    populateTreatment()
