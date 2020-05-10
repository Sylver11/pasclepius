from application.db_utils import pool
from datetime import datetime

def get_index(medical, date):
    date = datetime.strptime(date, '%d.%m.%Y')
    month = date.month
    year = date.year
    sql = """SELECT COUNT(*) FROM andrea_invoice WHERE medical = '{}' AND YEAR
    (date) = '{}' AND MONTH(date) = '{}'""".format(medical, year, month)
    conn = pool.connection()
    cursor = conn.cursor()
    cursor.execute(sql)
    index = cursor.fetchone()
    cursor.close()
    conn.close()
    return index['COUNT(*)'] + 1


def liveSearch(name):
    sql = """SELECT name FROM andrea_invoice WHERE name LIKE '{}%'
    """.format(name)
    conn = pool.connection()
    cursor = conn.cursor()
    cursor.execute(sql)
    data = cursor.fetchall()
    cursor.close()
    conn.close()
    return data


def getInvoiceURL(name, date):
    date = datetime.strptime(date, '%d.%m.%Y')
    sql = """SELECT url FROM andrea_invoice WHERE name = '{}' AND date =
    '{}'""".format(name, date)
    conn = pool.connection()
    cursor = conn.cursor()
    cursor.execute(sql)
    url = cursor.fetchone()
    cursor.close()
    conn.close()
    return url


def queryInvoice(patient):
    sql = """SELECT * FROM andrea_invoice WHERE name = '{}' """.format(patient)
    conn = pool.connection()
    cursor = conn.cursor()
    cursor.execute(sql)
    data = cursor.fetchall()
    cursor.close()
    conn.close()
    return data

def getSingleInvoice(patient, date):
    sql = """SELECT * FROM andrea_invoice WHERE name = '{}' AND date = '{}'
    """.format(patient, date)
    conn = pool.connection()
    cursor = conn.cursor()
    cursor.execute(sql)
    data = cursor.fetchone()
    cursor.close()
    conn.close()
    return data




def updateInvoice(treatments, dates, patient):
    name = patient['name']
    date = patient['date']
    treatments = ','.join(map(str, treatments))
    dates = ','.join(map(str, dates))
    date = datetime.strptime(date, '%d.%m.%Y')
    print(treatments)
    print(dates)
    sql = """UPDATE andrea_invoice SET treatments = '{}', dates = '{}' WHERE
    name = '{}' AND date = '{}'""".format(treatments, dates, name, date)
    conn = pool.connection()
    cursor = conn.cursor()
    cursor.execute(sql)
    cursor.close()
    conn.close()
    status = True
    return status



def add_invoice(patient, invoice, url, treatments, dates):
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
    treatments = ','.join(map(str, treatments))
    dates = ','.join(map(str, dates))
    sql = """INSERT INTO andrea_invoice (name, date, medical, invoice, url,
    treatments, dates, tariff, main, dob, number, `case`, po)
    VALUES('{0}','{1}','{2}','{3}','{4}','{5}','{6}','{7}','{8}','{9}','{10}','{11}','{12}')
    """.format(name, date, medical, invoice, url, treatments, dates, tariff, main, dob, number, case, po)
    sql_check_duplicate = """ SELECT * FROM andrea_invoice WHERE name='{}' AND date='{}'""".format(name, date)
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
