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

def add_invoice(patient, invoice):
    name = patient['name']
    date = patient['date']
    medical = patient['medical']
    tariff = patient['tariff']
    main = None
    dob = None
    number = None
    case = None
    po = 0
    if (medical == 'mva'):
        case = patient['case']
        po = patient['po']
    else:
        main = patient['main']
        dob = patient['dob']
        number = patient['number']

    date = datetime.strptime(date, '%d.%m.%Y')
    sql = """INSERT INTO andrea_invoice (name, date, medical, invoice, tariff,
    main, dob, number, `case`, po)
    VALUES('{0}','{1}','{2}','{3}','{4}','{5}','{6}','{7}','{8}','{9}')
    """.format(name, date, medical, invoice, tariff, main, dob, number, case, po)
    conn = pool.connection()
    cursor = conn.cursor()
    cursor.execute(sql)
    cursor.close()
    conn.close()

if __name__ == '__main__':
    from dotenv import load_dotenv
    load_dotenv()
    from db_utils import pool
    get_index('mva','30.04.2020')
    #add_invoice("JustusVoigt",'14.04.2020', 'mva', 'MVA/2020/4-1', 'namaf_physio_2019', case='bl23424', po='123132')
