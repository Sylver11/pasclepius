from application.db_utils import pool
from datetime import datetime

def get_index(uuid, medical_aid, date):
    date = datetime.strptime(date, '%d.%m.%Y')
    month = date.month
    year = date.year
    sql = """SELECT COUNT(*) FROM invoices WHERE uuid_text = '{}' AND  medical_aid = '{}' AND YEAR
    (date_created) = '{}' AND MONTH(date_created) = '{}'""".format(uuid, medical_aid, year, month)
    conn = pool.connection()
    cursor = conn.cursor()
    cursor.execute(sql)
    index = cursor.fetchone()
    cursor.close()
    conn.close()
    return index['COUNT(*)'] + 1


def liveSearch(uuid, patient_name):
    sql = """SELECT DISTINCT patient_name FROM invoices WHERE uuid_text = '{}' AND patient_name LIKE '{}%'
    """.format(uuid, patient_name)
    conn = pool.connection()
    cursor = conn.cursor()
    cursor.execute(sql)
    data = cursor.fetchall()
    cursor.close()
    conn.close()
    return data

def liveSearchInvoices(uuid, patient_name):
    sql = """SELECT any_value(invoices.invoice_id) AS invoice_id,
    any_value(invoices.patient_name) AS patient_name,
    any_value(invoices.credit_cent) AS credit_cent,
    any_value(invoices.submitted_on) AS submitted_on,
    any_value(invoices.date_created) AS date_created,
    any_value(invoices.date_invoice) AS date_invoice,
    group_concat(invoice_items.item) AS item_numbers,
    group_concat(invoice_items.units) AS item_units,
    group_concat(invoice_items.description) AS item_descriptions,
    group_concat(invoice_items.value_cent) AS item_values,
    group_concat(invoice_items.post_value_cent) AS item_post_values,
    group_concat(invoice_items.date) AS item_dates,
    group_concat(invoice_items.status) AS item_status
    FROM invoices LEFT JOIN invoice_items
    ON invoice_items.invoice_id = invoices.invoice_id
    WHERE invoices.uuid_text = '{}' AND invoices.patient_name LIKE '{}%'
    GROUP BY invoices.invoice_id""".format(uuid, patient_name)
    conn = pool.connection()
    cursor = conn.cursor()
    cursor.execute(sql)
    data = cursor.fetchall()
    cursor.close()
    conn.close()
    return data

def getPatient(uuid, patient_name):
    sql = """ SELECT any_value(tariff) AS tariff, any_value(patient_birth_date) AS
    patient_birth_date,
    any_value(medical_number) AS medical_number, any_value(medical_aid) AS medical_aid, any_value(case_number) AS case_number, any_value(main_member) AS main_member,
    patient_name FROM
    invoices WHERE uuid_text = '{}' AND patient_name = '{}' GROUP BY CASE WHEN
    medical_aid = 'mva' THEN `case_number` ELSE medical_number END;""".format(uuid, patient_name)
    conn = pool.connection()
    cursor = conn.cursor()
    cursor.execute(sql)
    patient_data = cursor.fetchall()
    cursor.close()
    conn.close()
    return patient_data


def getInvoiceURL(uuid, name_patient, date):
    date = datetime.strptime(date, '%d.%m.%Y')
    sql = """SELECT invoice_file_url FROM invoices WHERE uuid_text = '{}' AND name_patient = '{}'
    AND date_created = '{}'""".format(uuid, name_patient, date)
    conn = pool.connection()
    cursor = conn.cursor()
    cursor.execute(sql)
    invoice_file_url = cursor.fetchone()
    cursor.close()
    conn.close()
    return invoice_file_url


def queryInvoice(uuid, patient):
    sql = """SELECT * FROM invoices WHERE uuid_text = '{}' AND patient_name = '{}'
    """.format(uuid, patient)
    conn = pool.connection()
    cursor = conn.cursor()
    cursor.execute(sql)
    data = cursor.fetchall()
    cursor.close()
    conn.close()
    return data


def getSingleInvoice(uuid, invoice_id=None, patient=None, date=None):
    sql = ''
    if invoice_id:
        sql = """SELECT *
        FROM invoices WHERE uuid_text = '{}' AND invoice_id = '{}'
        """.format(uuid, invoice_id)
    else:
        sql = """SELECT * FROM invoices WHERE uuid_text = '{}'
        AND patient_name = '{}' AND
        date_created = '{}'
        """.format(uuid, patient, date)
    conn = pool.connection()
    cursor = conn.cursor()
    cursor.execute(sql)
    invoice = cursor.fetchone()
    cursor.close()
    conn.close()
    return invoice


def getItems(uuid, invoice_id):
    sql = """SELECT * FROM invoice_items WHERE uuid_text = '{}' AND invoice_id
    = '{}'""".format(uuid, invoice_id)
    conn = pool.connection()
    cursor = conn.cursor()
    cursor.execute(sql)
    items = cursor.fetchall()
    cursor.close()
    conn.close()
    return items

#def getInvoiceByInvoiceName(uuid, invoice_id):
#    sql = """SELECT *
#    FROM invoices WHERE uuid_text = '{}' AND invoice_id = '{}'
#    """.format(uuid, invoice_id)
#    conn = pool.connection()
#    cursor = conn.cursor()
#    cursor.execute(sql)
#    invoice = cursor.fetchone()
#    cursor.close()
#    conn.close()
#    return invoice

def getAllInvoices(uuid, c_option=None, r_option=None, 
        focus= None, order=None, start=None, range=None):
    if c_option == 'None' or r_option == 'None':
        c_option = 'uuid_text'
        r_option = uuid
    if(start and range and focus and order and c_option and r_option):
        sql = """SELECT patient_name, date_created, date_invoice, remind_me, credit_cent,
        submitted_on, medical_aid, invoice_id,invoice_file_url, tariff, status,
        main_member, patient_birth_date, medical_number, po_number,`case_number`,
        (SELECT COUNT('patient_name') FROM invoices WHERE uuid_text = '{}' AND 
        {} = '{}' ) AS rowcounter,
        (SELECT SUM(post_value_cent) FROM invoice_items WHERE uuid_text = '{}' AND
        invoice_id = invoices.invoice_id) AS debit_cent FROM invoices WHERE uuid_text = '{}'
        AND {} = '{}' ORDER BY {} {} LIMIT {},{}
        """.format(uuid, c_option, r_option, uuid, uuid, c_option, r_option, focus, order,  start, range)
    else:
        sql = """SELECT patient_name, date_created, date_invoice, remind_me, credit_cent,
        submitted_on, medical_aid, invoice_id,invoice_file_url, tariff,
        main_member, patient_birth_date, medical_number, po_number,`case_number` FROM invoices WHERE uuid_text = '{}'
        """.format(uuid)
    conn = pool.connection()
    cursor = conn.cursor()
    cursor.execute(sql)
    data = cursor.fetchall()
    cursor.close()
    conn.close()
    return data

def queryR(uuid, c_option):
    sql = """SELECT DISTINCT {} FROM invoices WHERE uuid_text = '{}'
        """.format(c_option, uuid)
    conn = pool.connection()
    cursor = conn.cursor()
    cursor.execute(sql)
    r_option = cursor.fetchall()
    cursor.close()
    conn.close()
    return r_option


def updateSubmitted(uuid, invoice_id):
    sql= """UPDATE invoices SET submitted_on = NOW(), status = 'due' WHERE uuid_text = '{}' and
    invoice_id = '{}'""".format(uuid, invoice_id)
    conn = pool.connection()
    cursor = conn.cursor()
    cursor.execute(sql)
    cursor.close()
    conn.close()
    status = True
    return status


def updateCredit(uuid, invoice_id, credit_cent):
    sql = """UPDATE invoices
    SET credit_cent = credit_cent + '{}'
    WHERE uuid_text = '{}' AND invoice_id =
    '{}'""".format(credit_cent, uuid, invoice_id)
    conn = pool.connection()
    cursor = conn.cursor()
    cursor.execute(sql)
    cursor.close()
    conn.close()
    status = True
    return status

def updateInvoice(user, patient, date_invoice, item_numbers, item_descriptions, item_values, item_dates, item_modifiers):
    hospital_name = procedure = diagnosis = implants = intra_op = post_op = None
    procedure_date = diagnosis_date = admission_date = discharge_date = datetime.strptime('1000-01-01 00:00:00', '%Y-%m-%d %H:%M:%S')
    date_created = datetime.strptime(patient['date_created'], '%d.%m.%Y')
    date_invoice = datetime.strptime(date_invoice[0], '%d.%m.%Y')

    if (4 <= user['invoice_layout'] <= 9):
        hospital_name = patient['hospital_name']
        admission_date = patient['admission_date']
        discharge_date = patient['discharge_date']
    if (7 <= user['invoice_layout'] <= 12):
        procedure = patient['procedure']
        procedure_date = patient['procedure_date']
        diagnosis = patient['diagnosis']
        diagnosis_date = patient['diagnosis_date']
        implants = patient['implants']
        intra_op = patient['intra_op']
        post_op = patient['post_op']

    sql = """UPDATE invoices SET date_invoice = '{}', hospital_name = '{}',
    admission_date = '{}', discharge_date = '{}', `procedure` = '{}',
    procedure_date = '{}', diagnosis = '{}', diagnosis_date = '{}',
    implants = '{}', intra_op ='{}', post_op = '{}' WHERE
    uuid_text = '{}' AND invoice_id = '{}'""".format(date_invoice, hospital_name, admission_date, discharge_date, procedure,
            procedure_date, diagnosis, diagnosis_date, implants,
            intra_op, post_op, user['uuid_text'], patient['invoice_id'])
    if not item_modifiers:
        item_modifiers = [0] * len(item_numbers)
    item_dates = [d.replace(d, str(datetime.strptime(d, '%d.%m.%Y'))) for d in item_dates]
    list = []
    for i in range(len(item_descriptions)):
        list_item = []
        item_value_cent = float(item_values[i]) * 100
        list_item.extend((user['uuid_text'], patient['invoice_id'], item_numbers[i],
            item_descriptions[i]['units'], item_descriptions[i]['description'],
            item_descriptions[i]['value_cent'], item_value_cent, item_dates[i],
            item_modifiers[i]))
        list_item = tuple(list_item)
        list.append(list_item)
    sql_rm_invoice_items = """DELETE FROM invoice_items WHERE uuid_text = '{}' AND invoice_id = '{}'""".format(user['uuid_text'], patient['invoice_id'])
    sql_add_invoice_items = "INSERT INTO invoice_items (uuid_text, invoice_id, item, units, description, value_cent, post_value_cent, date, modifier) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
    conn = pool.connection()
    cursor = conn.cursor()
    cursor.execute(sql_rm_invoice_items)
    cursor.executemany(sql_add_invoice_items, list)
    cursor.execute(sql)
    cursor.close()
    conn.close()
    status = True
    return status


def add_invoice(user, patient, invoice_id, invoice_file_url, date_invoice, item_numbers, item_descriptions, item_values, item_dates, item_modifiers):
    patient_name = patient['patient_name']
    medical_aid = patient['medical_aid']
    tariff = patient['tariff']
    po_number = 0
    status = patient_birth_date = case_number = medical_number = main_member = None
    hospital_name = None
    patient_birth_date = procedure_date = diagnosis_date = admission_date = discharge_date = datetime.strptime('1000-01-01 00:00:00', '%Y-%m-%d %H:%M:%S')
    procedure = diagnosis = None
    implants = intra_op = post_op = None
    if (4 <= user['invoice_layout'] <= 9):
        hospital_name = patient['hospital_name']
        admission_date = patient['admission_date']
        discharge_date = patient['discharge_date']

    if (7 <= user['invoice_layout'] <= 12):
        procedure = patient['procedure']
        procedure_date = patient['procedure_date']
        diagnosis = patient['diagnosis']
        diagnosis_date = patient['diagnosis_date']
        implants = patient['implants']
        intra_op = patient['intra_op']
        post_op = patient['post_op']

    if (medical_aid == 'mva'):
        case_number = patient['case_number']
        po_number = patient['po_number']
    else:
        main_member = patient['main_member']
        patient_birth_date = patient['patient_birth_date']
        patient_birth_date = datetime.strptime(patient_birth_date, '%d.%m.%Y')
        medical_number = patient['medical_number']
    date_created = datetime.strptime(patient['date_created'], '%d.%m.%Y')
    date_invoice = datetime.strptime(date_invoice[0], '%d.%m.%Y')
    if not item_modifiers:
        item_modifiers = [0] * len(item_numbers)
    item_dates = [d.replace(d, str(datetime.strptime(d, '%d.%m.%Y'))) for d in item_dates]
    list = []
    for i in range(len(item_descriptions)):
        list_item = []
        item_value_cent = float(item_values[i]) * 100
        list_item.extend((user['uuid_text'], invoice_id, item_numbers[i],
            item_descriptions[i]['units'], item_descriptions[i]['description'],
            item_descriptions[i]['value_cent'], item_value_cent, item_dates[i],
            item_modifiers[i]))
        list_item = tuple(list_item)
        list.append(list_item)
    sql_individual_item = "INSERT INTO invoice_items (uuid_text, invoice_id, item, units, description, value_cent, post_value_cent, date, modifier) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
    sql_check_duplicate = """ SELECT * FROM invoices WHERE uuid_text='{}' AND
    patient_name='{}' AND date_created='{}'""".format(user['uuid_text'], patient['patient_name'], date_created)
    conn = pool.connection()
    cursor = conn.cursor()
    cursor.execute(sql_check_duplicate)
    rows = cursor.fetchall()
    if not rows:
        cursor.execute("""INSERT INTO invoices (uuid_text,
    patient_name, date_created, date_invoice, medical_aid,
    invoice_id, invoice_file_url, tariff, main_member,
    patient_birth_date, medical_number, `case_number`, po_number,
    hospital_name, admission_date, discharge_date, `procedure`,
    procedure_date, diagnosis, diagnosis_date,
    implants, intra_op, post_op)
    VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
    """,(user['uuid_text'], patient_name, date_created, date_invoice, medical_aid,
        invoice_id, invoice_file_url, tariff, main_member, patient_birth_date,
        medical_number, case_number, po_number, hospital_name, admission_date,
        discharge_date, procedure, procedure_date, diagnosis, diagnosis_date,
        implants, intra_op, post_op))
        cursor.executemany(sql_individual_item, list)
        status = True
    else:
        status = False
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
    prices = ['3688.10', '1432.30', '3917.30', '447.60']
    dates = ['15.07.2020', '22.07.2020', '16.07.2020', '15.07.2020']
    date_invoice = ['07.07.2020']
    uuid = 'E7D76BE4-BA3E-11EA-BCD1-0AE0AFC200E9'
    add_invoice(layout, patient, invoice_id, invoice_file_url, modifiers, treatments, prices, dates, date_invoice, uuid)
