from application.db_utils import pool
from datetime import datetime

def get_user(user):
    sql = """SELECT * FROM users WHERE name = '{}' AND date = '{}'
    """.format(user)
    conn = pool.connection()
    cursor = conn.cursor()
    cursor.execute(sql)
    data = cursor.fetchone()
    cursor.close()
    conn.close()
    return data


def checkDuplicateUsername(username):
    sql_check_duplicate = """SELECT * FROM users WHERE
    username='{}'""".format(username)
    conn = pool.connection()
    cursor = conn.cursor()
    cursor.execute(sql_check_duplicate)
    rows = cursor.fetchall()
    if not rows:
        status = True
    else:
        status = False
    cursor.close()
    conn.close()
    return status


def checkDuplicateEmail(email):
    sql_check_duplicate = """SELECT * FROM users WHERE
    email='{}'""".format(email)
    conn = pool.connection()
    cursor = conn.cursor()
    cursor.execute(sql_check_duplicate)
    rows = cursor.fetchall()
    if not rows:
        status = True
    else:
        status = False
    cursor.close()
    conn.close()
    return status



def updateUser(treatments, dates, patient):
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


def addUser(title, name, email, password, phone, cell, fax, address, bank_holder, bank_account, bank,
            bank_branch, practice_number, practice_name, hpcna_number,
            qualification, specialisation):
    sql = """INSERT INTO users (title, name, email, password, phone, cell, fax, address,
    bank_holder, bank_account, bank, bank_branch, practice_number, practice_name,
    hpcna_number, qualification, specialisation)
    VALUES('{0}','{1}','{2}','{3}','{4}','{5}','{6}','{7}','{8}','{9}','{10}','{11}','{12}','{13}','{14}','{15}','{16}')
    """.format(title, name, email, password, phone, cell, fax, address, bank_holder, bank_account,
               bank, bank_branch, practice_number, practice_name, hpcna_number,
              qualification, specialisation)
    conn = pool.connection()
    cursor = conn.cursor()
    cursor.execute(sql)
    status = True
    cursor.close()
    conn.close()
    return status


if __name__ == '__main__':
    from dotenv import load_dotenv
    load_dotenv()
    from db_utils import pool
    get_index('mva','30.04.2020')
    #add_invoice("JustusVoigt",'14.04.2020', 'mva', 'MVA/2020/4-1', 'namaf_physio_2019', case='bl23424', po='123132')
