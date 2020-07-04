from application.db_utils import pool
from datetime import datetime


def get_index(uuid, medical, date):
    date = datetime.strptime(date, '%d.%m.%Y')
    month = date.month
    year = date.year
    sql = """SELECT COUNT(*) FROM invoices WHERE uuid_text = '{}' AND  medical = '{}' AND YEAR
    (date_created) = '{}' AND MONTH(date_created) = '{}'""".format(uuid, medical, year, month)
    conn = pool.connection()
    cursor = conn.cursor()
    cursor.execute(sql)
    index = cursor.fetchone()
    cursor.close()
    conn.close()
    return index['COUNT(*)'] + 1


def liveSearch(uuid, name):
    sql = """SELECT DISTINCT name FROM invoices WHERE uuid_text = '{}' AND name LIKE '{}%'
    """.format(uuid, name)
    conn = pool.connection()
    cursor = conn.cursor()
    cursor.execute(sql)
    data = cursor.fetchall()
    cursor.close()
    conn.close()
    return data

def liveSearchInvoices(uuid, name):
    sql = """SELECT * FROM invoices WHERE uuid_text = '{}' AND name LIKE '{}%'
    """.format(uuid, name)
    conn = pool.connection()
    cursor = conn.cursor()
    cursor.execute(sql)
    data = cursor.fetchall()
    cursor.close()
    conn.close()
    return data

def getPatient(uuid, name):
    sql = """ SELECT any_value(tariff) AS tariff, any_value(dob) AS dob,
    any_value(number) AS number, any_value(medical) AS medical,
    any_value(`case`) AS `case`, any_value(main) AS main, name FROM
    invoices WHERE uuid_text = '{}' AND name = '{}' GROUP BY CASE WHEN
    medical = 'mva' THEN `case` ELSE number END;""".format(uuid, name)
    conn = pool.connection()
    cursor = conn.cursor()
    cursor.execute(sql)
    patient_data = cursor.fetchall()
    cursor.close()
    conn.close()
    return patient_data


def getInvoiceURL(uuid, name, date):
    date = datetime.strptime(date, '%d.%m.%Y')
    sql = """SELECT url FROM invoices WHERE uuid_text = '{}' AND name = '{}'
    AND date_created = '{}'""".format(uuid, name, date)
    conn = pool.connection()
    cursor = conn.cursor()
    cursor.execute(sql)
    url = cursor.fetchone()
    cursor.close()
    conn.close()
    return url


def queryInvoice(uuid, patient):
    sql = """SELECT * FROM invoices WHERE uuid_text = '{}' AND name = '{}'
    """.format(uuid, patient)
    conn = pool.connection()
    cursor = conn.cursor()
    cursor.execute(sql)
    data = cursor.fetchall()
    cursor.close()
    conn.close()
    return data


def getSingleInvoice(uuid, patient, date):
    sql = """SELECT *
    FROM invoices WHERE uuid_text = '{}' AND name = '{}' AND
    date_created = '{}'
    """.format(uuid, patient, date)
    conn = pool.connection()
    cursor = conn.cursor()
    cursor.execute(sql)
    data = cursor.fetchone()
    cursor.close()
    conn.close()
    return data


def getInvoiceByInvoiceName(uuid, invoice_name):
    sql = """SELECT *
    FROM invoices WHERE uuid_text = '{}' AND invoice = '{}'
    """.format(uuid, invoice_name)
    conn = pool.connection()
    cursor = conn.cursor()
    cursor.execute(sql)
    invoice = cursor.fetchone()
    cursor.close()
    conn.close()
    return invoice

def getAllInvoices(uuid):
    sql = """SELECT name, date_created, date_invoice, remind_me, credit,
    submitted_on, medical, invoice,url, `values`, treatments, dates, tariff,
    main, dob, number, po,`case` FROM invoices WHERE uuid_text = '{}'
    """.format(uuid)
    conn = pool.connection()
    cursor = conn.cursor()
    cursor.execute(sql)
    data = cursor.fetchall()
    cursor.close()
    conn.close()
    return data


def updateSubmitted(uuid, invoice_name):
    sql= """UPDATE invoices SET submitted_on = NOW() WHERE uuid_text = '{}' and
    invoice = '{}'""".format(uuid, invoice_name)
    conn = pool.connection()
    cursor = conn.cursor()
    cursor.execute(sql)
    #data = cursor.fetchall()
    cursor.close()
    conn.close()
    status = True
    return status


def updateCredit(uuid, invoice_name, credit):
    sql = """UPDATE invoices SET `credit` =  CASE WHEN `credit` IS NOT NULL THEN
    `credit` + '{}' ELSE '{}' END WHERE uuid_text = '{}' AND invoice =
    '{}'""".format(credit, credit, uuid, invoice_name)
    conn = pool.connection()
    cursor = conn.cursor()
    cursor.execute(sql)
    cursor.close()
    conn.close()
    print(sql)
    status = True
    return status

def updateInvoice(layout, uuid, modifiers, treatments, prices, dates, patient, date_invoice):
    name = patient['name']
    date = patient['date_created']
    hospital = admission = discharge = None
    procedure = procedure_date = diagnosis = diagnosis_date = None
    implants = intra_op = post_op = None 
    if (4 <= layout <= 9):
        hospital = patient['hospital']
        admission = patient['admission']
        discharge = patient['discharge']

    if (7 <= layout <= 12):
        procedure = patient['procedure']
        procedure_date = patient['procedure_date']
        diagnosis = patient['diagnosis']
        diagnosis_date = patient['diagnosis_date']
        implants = patient['implants']
        intra_op = patient['intra_op']
        post_op = patient['post_op']
    modifiers = ','.join(map(str, modifiers))
    treatments = ','.join(map(str, treatments))
    prices = ','.join(map(str, prices))
    dates = ','.join(map(str, dates))
    date = datetime.strptime(date, '%d.%m.%Y')
    date_invoice = datetime.strptime(date_invoice[0], '%d.%m.%Y')
    sql = """UPDATE invoices SET date_invoice = '{}', modifiers = '{}',
    treatments = '{}', `values` = '{}', dates = '{}', hospital = '{}',
    admission = '{}', discharge = '{}', `procedure` = '{}',
    procedure_date = '{}', diagnosis = '{}', diagnosis_date = '{}',
    implants = '{}', intra_op ='{}', post_op = '{}' WHERE
    uuid_text = '{}' AND name = '{}' AND date_created =
    '{}'""".format(date_invoice, modifiers, treatments, prices,
            dates, hospital, admission, discharge, procedure,
            procedure_date, diagnosis, diagnosis_date, implants,
            intra_op, post_op, uuid, name, date)
    conn = pool.connection()
    cursor = conn.cursor()
    cursor.execute(sql)
    cursor.close()
    conn.close()
    status = True
    return status


def add_invoice(layout, patient, invoice, url, modifiers, treatments, prices, dates, date_invoice, uuid):
    name = patient['name']
    date = patient['date_created']
    medical = patient['medical']
    tariff = patient['tariff']
    po = 0
    status = dob = case = number = main = None
    hospital = admission = discharge = None
    procedure = procedure_date = diagnosis = diagnosis_date = None
    implants = intra_op = post_op = None 
    if (4 <= layout <= 9):
        hospital = patient['hospital']
        admission = patient['admission']
        discharge = patient['discharge']

    if (7 <= layout <= 12):
        procedure = patient['procedure']
        procedure_date = patient['procedure_date']
        diagnosis = patient['diagnosis']
        diagnosis_date = patient['diagnosis_date']
        implants = patient['implants']
        intra_op = patient['intra_op']
        post_op = patient['post_op']

    if (medical == 'mva'):
        case = patient['case']
        po = patient['po']
    else:
        main = patient['main']
        dob = patient['dob']
        number = patient['number']
    date = datetime.strptime(date, '%d.%m.%Y')
    date_invoice = datetime.strptime(date_invoice[0], '%d.%m.%Y')
    modifiers = ','.join(map(str, modifiers))
    treatments = ','.join(map(str, treatments))
    prices = ','.join(map(str, prices))
    dates = ','.join(map(str, dates))
    sql = """INSERT INTO invoices (uuid_text,
    name, date_created, date_invoice, medical,
    invoice, url, modifiers, treatments,`values`,
    dates, tariff, main, dob, number, `case`, po,
    hospital, admission, discharge, `procedure`,
    procedure_date, diagnosis, diagnosis_date,
    implants, intra_op, post_op)
    VALUES('{0}','{1}','{2}','{3}','{4}','{5}',
    '{6}','{7}','{8}','{9}','{10}','{11}','{12}',
    '{13}','{14}','{15}','{16}','{17}','{18}','{19}',
    '{20}','{21}','{22}','{23}','{24}','{25}','{26}')
    """.format(uuid, name, date, date_invoice, medical,
        invoice, url, modifiers, treatments,prices,
        dates, tariff, main, dob, number, case, po,
        hospital, admission, discharge, procedure,
        procedure_date, diagnosis, diagnosis_date,
        implants, intra_op, post_op)
    sql_check_duplicate = """ SELECT * FROM invoices WHERE uuid_text='{}' AND
    name='{}' AND date_created='{}'""".format(uuid, name, date)
    conn = pool.connection()
    cursor = conn.cursor()
    cursor.execute(sql_check_duplicate)
    rows = cursor.fetchall()
    if not rows:
        cursor.execute(sql)
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
    get_index('mva','30.04.2020')
    #add_invoice("JustusVoigt",'14.04.2020', 'mva', 'MVA/2020/4-1', 'namaf_physio_2019', case='bl23424', po='123132')
