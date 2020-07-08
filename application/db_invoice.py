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
    sql = """SELECT * FROM invoices WHERE uuid_text = '{}' AND patient_name LIKE '{}%'
    """.format(uuid, patient_name)
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

def getInvoiceByInvoiceName(uuid, invoice_id):
    sql = """SELECT *
    FROM invoices WHERE uuid_text = '{}' AND invoice_id = '{}'
    """.format(uuid, invoice_id)
    conn = pool.connection()
    cursor = conn.cursor()
    cursor.execute(sql)
    invoice = cursor.fetchone()
    cursor.close()
    conn.close()
    return invoice

def getAllInvoices(uuid, c_option=None, r_option=None, 
        focus= None, order=None, start=None, range=None):
    if c_option == 'None' or r_option == 'None':
        c_option = 'uuid_text'
        r_option = uuid
    if(start and range and focus and order and c_option and r_option):
        sql = """SELECT patient_name, date_created, date_invoice, remind_me, credit,
        submitted_on, medical_aid, invoice_id,invoice_file_url, `values`, treatments, dates, tariff,
        main_member, patient_birth_date, medical_number, po_number,`case_number`,
        (SELECT COUNT('patient_name') FROM invoices WHERE uuid_text = '{}' AND {} = '{}' ) 
        as rowcounter
        FROM invoices WHERE uuid_text = '{}'
        AND {} = '{}' ORDER BY {} {} LIMIT {},{}
        """.format(uuid, c_option, r_option, uuid, c_option, r_option, focus, order,  start, range)
    else:
        sql = """SELECT patient_name, date_created, date_invoice, remind_me, credit,
        submitted_on, medical_aid, invoice_id,invoice_file_url, `values`, treatments, dates, tariff,
        main_member, patient_birth_date, medical_number, po_number,`case_number` FROM invoices WHERE uuid_text = '{}'
        """.format(uuid)
    print(sql)
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


def updateCredit(uuid, invoice_id, credit):
    sql = """UPDATE invoices SET `credit` =  CASE WHEN `credit` IS NOT NULL THEN
    `credit` + '{}' ELSE '{}' END WHERE uuid_text = '{}' AND invoice_id =
    '{}'""".format(credit, credit, uuid, invoice_id)
    conn = pool.connection()
    cursor = conn.cursor()
    cursor.execute(sql)
    cursor.close()
    conn.close()
    status = True
    return status

def updateInvoice(layout, uuid, modifiers, treatments, prices, dates, patient, date_invoice):
    patient_name = patient['patient_name']
    date = patient['date_created']
    invoice_id = patient['invoice_id']
   # po_number = 0
   # status = patient_birth_date = case_number = medical_number = main_member = None
    hospital_name = None
    procedure_date = diagnosis_date = admission_date = discharge_date = datetime.strptime('1000-01-01 00:00:00', '%Y-%m-%d %H:%M:%S')
    procedure = diagnosis = None
    implants = intra_op = post_op = None
   # hospital_name = admission_date = discharge_date = None
   # procedure = procedure_date = diagnosis = diagnosis_date = None
   # implants = intra_op = post_op = None 
    if (4 <= layout <= 9):
        hospital_name = patient['hospital_name']
        admission_date = patient['admission_date']
        discharge_date = patient['discharge_date']

    if (7 <= layout <= 12):
        procedure = patient['procedure']
        procedure_date = patient['procedure_date']
        diagnosis = patient['diagnosis']
        diagnosis_date = patient['diagnosis_date']
        implants = patient['implants']
        intra_op = patient['intra_op']
        post_op = patient['post_op']
   # modifiers = ','.join(map(str, modifiers))
   # treatments = ','.join(map(str, treatments))
   # prices = ','.join(map(str, prices))
   # dates = ','.join(map(str, dates))
    date = datetime.strptime(date, '%d.%m.%Y')
    date_invoice = datetime.strptime(date_invoice[0], '%d.%m.%Y')
    sql = """UPDATE invoices SET date_invoice = '{}', hospital_name = '{}',
    admission_date = '{}', discharge_date = '{}', `procedure` = '{}',
    procedure_date = '{}', diagnosis = '{}', diagnosis_date = '{}',
    implants = '{}', intra_op ='{}', post_op = '{}' WHERE
    uuid_text = '{}' AND patient_name = '{}' AND date_created =
    '{}'""".format(date_invoice, hospital_name, admission_date, discharge_date, procedure,
            procedure_date, diagnosis, diagnosis_date, implants,
            intra_op, post_op, uuid, patient_name, date)


    if not modifiers:
        modifiers = [0] * len(treatments)
    dates = [d.replace(d, str(datetime.strptime(d, '%d.%m.%Y'))) for d in dates]
    uuid_list = [uuid] * len(treatments)
    invoice_list = [invoice_id] * len(treatments)
    list_item = list(zip(uuid_list, invoice_list, treatments, prices, dates,
        modifiers))
    sql_rm_individual_item = """DELETE FROM invoice_items WHERE uuid_text = '{}'
    AND invoice_id = '{}'""".format(uuid, invoice_id)
    sql_individual_item = "INSERT INTO invoice_items (uuid_text, invoice_id, item, value, date, modifier) VALUES (%s, %s, %s, %s, %s, %s)"



    conn = pool.connection()
    cursor = conn.cursor()
    cursur.execute(sql_rm_individual_item)
    cursor.execute(sql_individual_item)
    cursor.execute(sql)
    cursor.close()
    conn.close()
    status = True
    return status


def add_invoice(layout, patient, invoice_id, invoice_file_url, modifiers, treatments, prices, dates, date_invoice, uuid):
    patient_name = patient['patient_name']
    date = patient['date_created']
    medical_aid = patient['medical_aid']
    tariff = patient['tariff']
    po_number = 0
    status = patient_birth_date = case_number = medical_number = main_member = None
    hospital_name = None
    patient_birth_date = procedure_date = diagnosis_date = admission_date = discharge_date = datetime.strptime('1000-01-01 00:00:00', '%Y-%m-%d %H:%M:%S')
    procedure = diagnosis = None
    implants = intra_op = post_op = None
    if (4 <= layout <= 9):
        hospital_name = patient['hospital_name']
        admission_date = patient['admission_date']
        discharge_date = patient['discharge_date']

    if (7 <= layout <= 12):
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
    date = datetime.strptime(date, '%d.%m.%Y')
    date_invoice = datetime.strptime(date_invoice[0], '%d.%m.%Y')
    sql = """INSERT INTO invoices (uuid_text,
    patient_name, date_created, date_invoice, medical_aid,
    invoice_id, invoice_file_url, tariff, main_member, patient_birth_date, medical_number, `case_number`, po_number,
    hospital_name, admission_date, discharge_date, `procedure`,
    procedure_date, diagnosis, diagnosis_date,
    implants, intra_op, post_op)
    VALUES('{0}','{1}','{2}','{3}','{4}','{5}',
    '{6}','{7}','{8}','{9}','{10}','{11}','{12}',
    '{13}','{14}','{15}','{16}','{17}','{18}','{19}',
    '{20}','{21}','{22}')
    """.format(uuid, patient_name, date, date_invoice, medical_aid,
        invoice_id, invoice_file_url, tariff, main_member, patient_birth_date, medical_number, case_number, po_number,
        hospital_name, admission_date, discharge_date, procedure,
        procedure_date, diagnosis, diagnosis_date,
        implants, intra_op, post_op)
    
    
    if not modifiers:
        modifiers = [0] * len(treatments)
    dates = [d.replace(d, str(datetime.strptime(d, '%d.%m.%Y'))) for d in dates]
    uuid_list = [uuid] * len(treatments)
    invoice_list = [invoice_id] * len(treatments)
    list_item = list(zip(uuid_list, invoice_list, treatments, prices, dates,
        modifiers))
    sql_individual_item = "INSERT INTO invoice_items (uuid_text, invoice_id, item, value, date, modifier) VALUES (%s, %s, %s, %s, %s, %s)"



    sql_check_duplicate = """ SELECT * FROM invoices WHERE uuid_text='{}' AND
    patient_name='{}' AND date_created='{}'""".format(uuid, patient_name, date)
    conn = pool.connection()
    cursor = conn.cursor()
    cursor.execute(sql_check_duplicate)
    rows = cursor.fetchall()
    if not rows:
        cursor.execute(sql)
        cursor.executemany(sql_individual_item, list_item)
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
