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
    sql = """SELECT name FROM invoices WHERE uuid_text = '{}' AND name LIKE '{}%'
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
    sql = """SELECT name, number, `case`, po, url, invoice,
    tariff, medical, dates, main, dob, treatments
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


def updateInvoice(uuid, treatments, dates, patient, date_invoice):
    name = patient['name']
    date = patient['date']
    treatments = ','.join(map(str, treatments))
    dates = ','.join(map(str, dates))
    date = datetime.strptime(date, '%d.%m.%Y')
    date_invoice = datetime.strptime(date_invoice[0], '%d.%m.%Y')
    sql = """UPDATE invoices SET date_invoice = '{}', treatments = '{}', dates = '{}' WHERE
    uuid_text = '{}' AND name = '{}' AND date_created =
    '{}'""".format(date_invoice, treatments, dates, uuid, name, date)
    conn = pool.connection()
    cursor = conn.cursor()
    cursor.execute(sql)
    cursor.close()
    conn.close()
    status = True
    return status


def add_invoice(patient, invoice, url, treatments, dates, date_invoice, uuid):
    name = patient['name']
    date = patient['date']
    medical = patient['medical']
    tariff = patient['tariff']
    main = None
    dob = None
    number = None
    case = None
    po = 0
    status = None
    if (medical == 'mva'):
        case = patient['case']
        po = patient['po']
    else:
        main = patient['main']
        dob = patient['dob']
        number = patient['number']
    date = datetime.strptime(date, '%d.%m.%Y')
    date_invoice = datetime.strptime(date_invoice[0], '%d.%m.%Y')
    treatments = ','.join(map(str, treatments))
    dates = ','.join(map(str, dates))
    sql = """INSERT INTO invoices (uuid_text, name, date_created, date_invoice, medical, invoice, url,
    treatments, dates, tariff, main, dob, number, `case`, po)
    VALUES('{0}','{1}','{2}','{3}','{4}','{5}','{6}','{7}','{8}','{9}','{10}','{11}','{12}','{13}','{14}')
    """.format(uuid, name, date, date_invoice, medical, invoice, url, treatments, dates, tariff, main, dob, number, case, po)
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
