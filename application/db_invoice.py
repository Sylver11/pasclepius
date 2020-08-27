from application.db_utils import pool
from datetime import date
from datetime import datetime
import simplejson as json

def get_index(practice_uuid, medical_aid):
    today = date.today()
    month = today.month
    year = today.year
    sql = """SELECT COUNT(*) FROM invoices WHERE practice_uuid = '{}' AND  medical_aid = '{}' AND YEAR
    (date_created) = '{}' AND MONTH(date_created) = '{}'""".format(practice_uuid, medical_aid, year, month)
    conn = pool.connection()
    cursor = conn.cursor()
    cursor.execute(sql)
    index = cursor.fetchone()
    cursor.close()
    conn.close()
    return index['COUNT(*)'] + 1


def liveSearchInvoices(practice_uuid, patient_name):
    sql = """SELECT 
    any_value(patients.practice_uuid) AS practice_uuid,
    any_value(patients.patient_name) AS patient_name,
    any_value(patients.patient_id) AS patient_id,
    any_value(invoices.invoice_id) AS invoice_id,
    any_value(invoices.credit_cent) AS credit_cent,
    any_value(invoices.submitted_on) AS submitted_on,
    any_value(invoices.date_created) AS date_created,
    any_value(invoices.date_invoice) AS date_invoice,
    any_value(invoices.status) AS status,
    group_concat(invoice_items.item) AS item_numbers,
    group_concat(invoice_items.units) AS item_units,
    group_concat(invoice_items.description) AS item_descriptions,
    group_concat(invoice_items.value_cent) AS item_values,
    group_concat(invoice_items.post_value_cent) AS item_post_values,
    group_concat(invoice_items.date) AS item_dates,
    group_concat(invoice_items.status) AS item_status
    FROM patients
    LEFT JOIN invoices
    ON invoices.patient_id = patients.patient_id
    LEFT JOIN invoice_items
    ON invoice_items.invoice_id = invoices.invoice_id
    WHERE patients.practice_uuid = '{}' AND patients.patient_name LIKE '{}%'
    GROUP BY invoices.invoice_id""".format(practice_uuid, patient_name)
    conn = pool.connection()
    cursor = conn.cursor()
    cursor.execute(sql)
    patient_invoices = cursor.fetchall()
    cursor.close()
    conn.close()
    return patient_invoices


def getInvoiceURL(practice_uuid, name_patient, date):
    sql = """SELECT invoice_file_url FROM invoices WHERE practice_uuid = '{}' AND name_patient = '{}'
    AND date_created = '{}'""".format(practice_uuid, name_patient, date)
    conn = pool.connection()
    cursor = conn.cursor()
    cursor.execute(sql)
    invoice_file_url = cursor.fetchone()
    cursor.close()
    conn.close()
    return invoice_file_url


def getSingleInvoice(practice_uuid, invoice_id):
    sql = """SELECT invoices.*, patients.*
        FROM invoices
        LEFT JOIN patients ON patients.patient_id = invoices.patient_id
        AND patients.practice_uuid = '{}' WHERE invoices.practice_uuid = '{}' AND
        invoices.invoice_id = '{}'
        """.format(practice_uuid, practice_uuid, invoice_id)
    conn = pool.connection()
    cursor = conn.cursor()
    cursor.execute(sql)
    invoice = cursor.fetchone()
    cursor.close()
    conn.close()
    return invoice


def getItems(practice_uuid, invoice_id):
    sql = """SELECT * FROM invoice_items WHERE practice_uuid = '{}' AND invoice_id
    = '{}'""".format(practice_uuid, invoice_id)
    conn = pool.connection()
    cursor = conn.cursor()
    cursor.execute(sql)
    items = cursor.fetchall()
    cursor.close()
    conn.close()
    return items


def queryInvoices(practice_uuid, c_option, r_option, focus, order, start, range):
    if c_option == 'None' or r_option == 'None':
        c_option = 'practice_uuid'
        r_option = practice_uuid
    sql = """SELECT invoices.patient_id, date_created, date_invoice, remind_me, credit_cent,
        submitted_on, invoice_id, invoice_file_url, tariff, status, po_number,
        (SELECT COUNT('patient_name') FROM invoices WHERE invoices.practice_uuid = '{}' AND
        invoices.{} = '{}' ) AS rowcounter,
        (SELECT SUM(post_value_cent) FROM invoice_items WHERE invoice_items.practice_uuid = '{}' AND
        invoice_items.invoice_id = invoices.invoice_id) AS debit_cent,
        patients.* FROM invoices
        LEFT JOIN patients ON patients.patient_id = invoices.patient_id
        AND patients.practice_uuid = '{}'
        WHERE invoices.practice_uuid = '{}'
        AND invoices.{} = '{}' ORDER BY {} {} LIMIT {},{}
        """.format(practice_uuid, c_option, r_option, practice_uuid, practice_uuid, practice_uuid, c_option, r_option, focus, order,  start, range)
    conn = pool.connection()
    cursor = conn.cursor()
    cursor.execute(sql)
    invoices = cursor.fetchall()
    cursor.close()
    conn.close()
    return invoices

def queryR(practice_uuid, c_option):
    sql = """SELECT DISTINCT {} FROM invoices WHERE practice_uuid = '{}'
        """.format(c_option, practice_uuid)
    conn = pool.connection()
    cursor = conn.cursor()
    cursor.execute(sql)
    r_option = cursor.fetchall()
    cursor.close()
    conn.close()
    return r_option


def updateSubmitted(practice_uuid, invoice_id):
    sql= """UPDATE invoices SET submitted_on = NOW(), status = 'due' WHERE practice_uuid = '{}' and
    invoice_id = '{}'""".format(practice_uuid, invoice_id)
    conn = pool.connection()
    cursor = conn.cursor()
    cursor.execute(sql)
    cursor.close()
    conn.close()
    status = True
    return status


def updateCredit(practice_uuid, invoice_id, credit_cent):
    sql = """UPDATE invoices
    SET credit_cent = credit_cent + '{}'
    WHERE practice_uuid = '{}' AND invoice_id =
    '{}'""".format(credit_cent, practice_uuid, invoice_id)
    conn = pool.connection()
    cursor = conn.cursor()
    cursor.execute(sql)
    cursor.close()
    conn.close()
    status = True
    return status


def insertInvoice(practice_uuid, user_name, invoice_form):
    conn = pool.connection()
    cursor = conn.cursor()
    status = {}
    cursor.execute("""INSERT INTO invoices (practice_uuid, last_edited_by,
        patient_id, date_invoice, medical_aid, invoice_id, invoice_file_url, tariff,
        invoice_layout, po_number, hospital_name, admission_date,
        discharge_date, `procedure`, procedure_date, diagnosis,
        diagnosis_date, implants, intra_op, post_op)
        VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
        """,(practice_uuid,
        user_name,
        invoice_form['patient_id'],
        invoice_form['date_invoice'],
        invoice_form['medical_aid'],
        invoice_form['invoice_id'],
        invoice_form['invoice_file_url'],
        invoice_form['tariff'],
        invoice_form['invoice_layout'],
        invoice_form.get('po_number') or None,
        invoice_form.get('hospital_name') or None,
        invoice_form.get('admission_date') or None,
        invoice_form.get('discharge_date') or None,
        invoice_form.get('procedure') or None,
        invoice_form.get('procedure_date') or None,
        invoice_form.get('diagnosis') or None,
        invoice_form.get('diagnosis_date') or None,
        invoice_form.get('implants') or None,
        invoice_form.get('intra_op') or None,
        invoice_form.get('post_op') or None))

    list = []
    for i in range(len(invoice_form.getlist('treatments'))):
        list_item = []
        list_item.extend((practice_uuid,
            invoice_form['invoice_id'],
            invoice_form.getlist('treatments')[i],
            float(invoice_form.getlist('units')[i]) * 100,
            invoice_form.getlist('description')[i],
            float(invoice_form.getlist('value')[i]) * 100,
            float(invoice_form.getlist('post_value')[i]) * 100,
            invoice_form.getlist('date')[i],
            invoice_form.getlist('modifier')[i]))
        list_item = tuple(list_item)
        list.append(list_item)
    sql_individual_item = """INSERT INTO invoice_items (practice_uuid,
        invoice_id, item, units, description, value_cent, post_value_cent,
        date, modifier) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"""
    cursor.executemany(sql_individual_item, list)

    status['db_status'] = 'Success'
    status['db_description'] = 'New invoice created ' + invoice_form['invoice_id']
    status['invoice_id'] = invoice_form['invoice_id']
    cursor.close()
    conn.close()
    return status

def updateInvoice(practice_uuid, user_name, invoice_form):
    conn = pool.connection()
    cursor = conn.cursor()
    status = {}
    sql = """UPDATE invoices SET po_number = %s, hospital_name = %s,
        admission_date = %s, discharge_date = %s,  `procedure` = %s,
        procedure_date = %s, diagnosis = %s, diagnosis_date = %s, implants = %s,
        intra_op = %s, post_op = %s, last_edited = NOW(), last_edited_by = %s WHERE practice_uuid =
        %s AND invoice_id = %s
        """
    invoice_form_tuple = (invoice_form.get('po_number') or None,
        invoice_form.get('hospital_name') or None,
        invoice_form.get('admission_date') or None,
        invoice_form.get('discharge_date') or None,
        invoice_form.get('procedure') or None,
        invoice_form.get('procedure_date') or None,
        invoice_form.get('diagnosis') or None,
        invoice_form.get('diagnosis_date') or None,
        invoice_form.get('implants') or None,
        invoice_form.get('intra_op') or None,
        invoice_form.get('post_op') or None,
        user_name,
        practice_uuid,
        invoice_form['invoice_id'])

    cursor.execute(sql, invoice_form_tuple)

    sql_rm_invoice_items = """DELETE FROM invoice_items WHERE practice_uuid = '{}'
    AND invoice_id = '{}'""".format(practice_uuid,
                invoice_form['invoice_id'])
    cursor.execute(sql_rm_invoice_items)
    list = []
    for i in range(len(invoice_form.getlist('treatments'))):
        list_item = []
        list_item.extend((practice_uuid,
            invoice_form['invoice_id'],
            invoice_form.getlist('treatments')[i],
            float(invoice_form.getlist('units')[i]) * 100,
            invoice_form.getlist('description')[i],
            float(invoice_form.getlist('value')[i]) * 100,
            float(invoice_form.getlist('post_value')[i]) * 100,
            invoice_form.getlist('date')[i],
            invoice_form.getlist('modifier')[i]))
        list_item = tuple(list_item)
        list.append(list_item)
    sql_individual_item = """INSERT INTO invoice_items (practice_uuid,
        invoice_id, item, units, description, value_cent, post_value_cent,
        date, modifier) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"""
    cursor.executemany(sql_individual_item, list)

    status['db_status'] =  'Success'
    status['db_description'] = 'Updated invoice'
    status['invoice_id'] = invoice_form['invoice_id']
    cursor.close()
    conn.close()
    return status

if __name__ == '__main__':
    from dotenv import load_dotenv
    load_dotenv()
    from db_utils import pool
    #get_index('mva','30.04.2020')
    layout = 3
    patient = {'admission_date': '', 'case_number': '234234',
            'date_created': '09.07.2020', 'diagnosis': '',
            'diagnosis_date': '', 'discharge_date': '', 'hospital_name': '',
            'implants': '', 'intra_op': '', 'medical_aid': 'mva',
            'patient_name': 'Thomas Mueller', 'po_number': 234234, 'post_op': '',
            'procedure': '', 'procedure_date': '', 'submit': True,
            'tariff': 'namaf_orthopaedic_surgeons_2020'}
    invoice_id = 'MVA/2020/7-5'
    invoice_file_url = '/home/practice/Documents/Juschdus sei super praxis/MVA_Justus2020/7July2020/7_5Thomas Mueller'
    modifiers = []
    treatments = ['503', '773', '1815', '2725']
    values = ['3688.10', '1432.30', '3917.30', '447.60']
    dates = ['15.07.2020', '22.07.2020', '16.07.2020', '15.07.2020']
    date_invoice = ['07.07.2020']
    uuid = 'E7D76BE4-BA3E-11EA-BCD1-0AE0AFC200E9'
    add_invoice(layout, patient, invoice_id, invoice_file_url, modifiers, treatments, values, dates, date_invoice, uuid)
