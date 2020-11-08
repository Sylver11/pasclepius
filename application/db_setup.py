import os
import pandas as pd


def setupTable():
    sql_drop_table_namaf_tariffs = "DROP TABLE IF EXISTS namaf_tariffs"
    sql_drop_table_invoice = "DROP TABLE IF EXISTS invoices"
    sql_drop_table_users = "DROP TABLE IF EXISTS users"
    sql_drop_table_invoice_items = "DROP TABLE IF EXISTS invoice_items"
    sql_drop_table_user_workbench = "DROP TABLE IF EXISTS user_workbench"
    sql_drop_table_patients = "DROP TABLE IF EXISTS patients"
    sql_drop_table_practice = "DROP TABLE IF EXISTS practices"
    sql_drop_table_practice_connections = "DROP TABLE IF EXISTS practice_connections"

    sql_create_table_namaf_tariffs = """CREATE TABLE namaf_tariffs  (
        id int(11) NOT NULL AUTO_INCREMENT,
        item int(11) NOT NULL,
        description TEXT NOT NULL,
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
        id int(11) NOT NULL AUTO_INCREMENT,
        practice_uuid varchar(36) NOT NULL,
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
        id int(11) NOT NULL AUTO_INCREMENT,
        practice_uuid varchar(36) NOT NULL,
        patient_id varchar(255) NOT NULL,
        medical_aid varchar(255) NOT NULL,
        date_created DATETIME NOT NULL DEFAULT NOW(),
        date_invoice DATE NOT NULL,
        invoice_id varchar(255) NOT NULL,
        invoice_file_url varchar(255) NOT NULL,
        tariff varchar(255) NOT NULL,
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
        last_edited DATETIME DEFAULT NOW(),
        last_edited_by VARCHAR(255),
        PRIMARY KEY (id));"""

    sql_create_table_patients = """ CREATE TABLE patients (
        id int(11) NOT NULL AUTO_INCREMENT,
        practice_uuid varchar(36) NOT NULL,
        patient_id varchar(255) GENERATED ALWAYS AS
            (CASE WHEN medical_number IS NULL THEN case_number ELSE
            medical_number END) VIRTUAL,
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
        id int(11) NOT NULL AUTO_INCREMENT,
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
        title varchar(255),
        first_name varchar(255) NOT NULL,
        second_name varchar(255) NOT NULL,
        email varchar(100) NOT NULL UNIQUE,
        current_practice_uuid varchar(36),
        current_practice_role varchar(255),
        created_on DATETIME NOT NULL DEFAULT NOW(),
        last_active DATETIME NOT NULL DEFAULT NOW(),
        PRIMARY KEY (id));"""

    sql_create_table_practice = """CREATE TABLE practices (
        id int(11) NOT NULL AUTO_INCREMENT,
        uuid_bin binary(16),
        practice_uuid varchar(36) generated always as
            (insert(
                insert(
                    insert(
                        insert(hex(uuid_bin),9,0,'-'),
                        14,0,'-'),
                    19,0,'-'),
                24,0,'-')
            ) virtual,
        practice_admin varchar(255) NOT NULL UNIQUE,
        practice_name varchar(255) NOT NULL,
        practice_number varchar(255) NOT NULL,
        namaf_profession varchar(255) NOT NULL,
        practice_email varchar(255) NOT NULL,
        phone varchar(255) NOT NULL,
        cell varchar(255),
        fax varchar(255),
        pob varchar(255),
        city varchar(255),
        country varchar(255),
        bank_holder varchar(255),
        bank_account varchar(255),
        bank varchar(255),
        bank_branch varchar(255),
        hpcna_number varchar(255),
        qualification varchar(255),
        specialisation varchar(255),
        practice_folder_id int(11) NOT NULL DEFAULT 0,
        premium BOOLEAN NOT NULL DEFAULT false,
        invoice_layout int(11) NOT NULL DEFAULT 1,
        created_on DATETIME NOT NULL DEFAULT NOW(),
        PRIMARY KEY (id));"""

    sql_create_table_practice_connections = """CREATE TABLE
    practice_connections (
    id int(11) NOT NULL AUTO_INCREMENT,
    practice_uuid varchar(36) NOT NULL,
    practice_name varchar(255) NOT NULL,
    user_uuid varchar(36) NOT NULL,
    user_email varchar(255) NOT NULL,
    user_name varchar(255) NOT NULL,
    practice_role varchar(255) NOT NULL,
    created_on DATETIME NOT NULL DEFAULT NOW(),
    PRIMARY KEY (id));"""

    sql_create_table_user_workbench = """CREATE TABLE user_workbench (
    uuid_text VARCHAR(36) NOT NULL,
    practice_uuid VARCHAR(36) NOT NULL,
    work_type VARCHAR(255) NOT NULL,
    work_quality TEXT NOT NULL,
    created_on DATETIME NOT NULL DEFAULT NOW());"""



    create_trigger_status = """CREATE TRIGGER check_settled BEFORE UPDATE ON invoices
    FOR EACH ROW
    BEGIN
    IF NEW.credit_cent = (SELECT SUM(post_value_cent) FROM invoice_items WHERE practice_uuid = OLD.practice_uuid AND invoice_id = OLD.invoice_id) THEN
    SET NEW.status = 'settled';
    ELSEIF NEW.credit_cent > (SELECT SUM(post_value_cent)
    FROM invoice_items WHERE practice_uuid = OLD.practice_uuid AND invoice_id =
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
    cursor.execute(sql_drop_table_practice)
    cursor.execute(sql_create_table_practice)
    cursor.execute(sql_drop_table_practice_connections)
    cursor.execute(sql_create_table_practice_connections)
    cursor.execute(sql_drop_table_users)
    cursor.execute(sql_drop_table_invoice)
    cursor.execute(sql_create_table_invoice)
    cursor.execute(sql_drop_table_namaf_tariffs)
    cursor.execute(sql_create_table_namaf_tariffs)
    cursor.execute(create_trigger_status)
    cursor.execute(sql_create_table_users)
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
    from dotenv import load_dotenv
    load_dotenv()
    from db_utils import pool
    setupTable()
    populateTreatment()
