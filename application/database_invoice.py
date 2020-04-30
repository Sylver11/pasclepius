from db_utils import pool

def get_index(medical, year, month):
    sql = """SELECT COUNT(*) FROM andrea_invoice WHERE medical = {} AND YEAR
    (date) = {} AND MONTH(date) = {}""".format(medical, year, month)
    conn = pool.connection()
    cursor = conn.cursor()
    cursor.execute(sql)
    index = cursor.fetchone()
    cursor.close()
    conn.close()
    return index

def add_invoice(name, date, medical, invoice, tariff, main=None, dob=None, number=None,case=None, po=None):
    sql = """INSERT INTO andrea_invoice (name, date, medical, invoice, tariff, main, dob, number, case, po)  VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s) """
    value = name, date, medical, invoice, tariff, main, dob, number, po
    conn = pool.connection()
    cursor = conn.cursor()
    cursor.execute(sql_insert, value)
    cursor.close()
    conn.close()

if __name__ == '__main__':
    from dotenv import load_dotenv
    load_dotenv()
