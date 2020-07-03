from application.db_utils import pool
from datetime import datetime

def checkUser(email):
    conn = pool.connection()
    cursor = conn.cursor()
    cursor.execute("""SELECT password, uuid_text, email, title, first_name, second_name, phone, cell, fax, pob, city, country, bank_holder,
    bank_account, bank_branch, bank, practice_name, practice_number,
    hpcna_number, qualification, specialisation, invoice_layout FROM users
    WHERE email =  %s""",(email))
    data = cursor.fetchone()
    cursor.close()
    conn.close()
    return data


def checkDuplicateEmail(email):
    sql_check_duplicate = """SELECT * FROM users WHERE
    email='{}'""".format(email)
    conn = pool.connection()
    cursor = conn.cursor()
    cursor.execute(sql_check_duplicate)
    rows = cursor.fetchall()
    if not rows:
        status = False
    else:
        status = True
    cursor.close()
    conn.close()
    return status


def updateUserPassword(email, password):
    sql = """UPDATE users SET password = '{}' WHERE
    email = '{}'""".format(password, email)
    conn = pool.connection()
    cursor = conn.cursor()
    cursor.execute(sql)
    cursor.close()
    conn.close()
    status = True
    return status

def updateUserLayout(email, phone, fax, hospital, diagnosis):
    if phone and fax and hospital and diagnosis:
        layout_code = 9
    elif phone and fax and hospital:
        layout_code = 6
    elif phone and fax and diagnosis:
        layout_code = 12
    elif phone and hospital and diagnosis:
        layout_code = 8
    elif phone and fax:
        layout_code = 3
    elif phone and hospital:
        layout_code = 5
    elif phone and diagnosis:
        layout_code = 11
    elif hospital and diagnosis:
        layout_code = 7
    elif phone:
        layout_code = 2
    elif hospital:
        layout_code = 4
    elif diagnosis:
        layout_code = 10
    else:
        layout_code = 1
    sql = """UPDATE users SET invoice_layout = '{}' WHERE
    email = '{}'""".format(layout_code, email)
    conn = pool.connection()
    cursor = conn.cursor()
    cursor.execute(sql)
    cursor.close()
    conn.close()
    status = True
    return status

def updateUserPractice(email, practice_name, practice_number, hpcna_number):
    sql = """ UPDATE users SET practice_name = '{}', practice_number = '{}',
    hpcna_number = '{}' WHERE email = '{}'""".format(practice_name,
            practice_number, hpcna_number, email)
    conn = pool.connection()
    cursor = conn.cursor()
    cursor.execute(sql)
    cursor.close()
    conn.close()
    status = True
    return status


def updateUserBanking(email, bank_holder, bank_account, bank_branch, bank):
    sql = """ UPDATE users SET bank_holder = '{}', bank_account = '{}',
    bank_branch = '{}', bank = '{}' WHERE email = '{}'""".format(bank_holder,
            bank_account, bank_branch, bank, email)
    conn = pool.connection()
    cursor = conn.cursor()
    cursor.execute(sql)
    cursor.close()
    conn.close()
    status = True
    return status



def updateUserPersonal(email, first_name, second_name, cell, pob, city,
        country,qualification,title=None,phone=None,fax=None,specialisation=None):
    sql = """UPDATE users SET first_name = '{}', second_name = '{}', cell =
    '{}', pob = '{}', city = '{}', country = '{}', qualification = '{}', title
    = '{}', phone = '{}', fax = '{}', specialisation = '{}' WHERE
    email = '{}'""".format(first_name, second_name, cell, pob, city, country,
            qualification, title, phone, fax, specialisation,  email)
    conn = pool.connection()
    cursor = conn.cursor()
    cursor.execute(sql)
    cursor.close()
    conn.close()
    status = True
    return status



def addUser(title, first_name, second_name, email, password, phone, cell, fax, pob, city, country, bank_holder, bank_account, bank,
            bank_branch, practice_number, practice_name, hpcna_number,
            qualification, specialisation):
    conn = pool.connection()
    cursor = conn.cursor()
    cursor.execute("""INSERT INTO users (uuid_bin, title, first_name, second_name, email, password, phone,
    cell, fax, pob, city, country,
    bank_holder, bank_account, bank,
    bank_branch, practice_number, practice_name,
    hpcna_number, qualification, specialisation)
    VALUES(unhex(replace(uuid(),'-','')),%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
    """,(title, first_name, second_name,
            email, password, phone, cell, fax,
            pob, city, country, bank_holder, bank_account,
            bank, bank_branch, practice_number, practice_name, hpcna_number,
            qualification, specialisation))
    status = True
    cursor.close()
    conn.close()
    return status


if __name__ == '__main__':
    from dotenv import load_dotenv
    load_dotenv()
    from db_utils import pool
    addUser("Dr", "Justus Voigt",'justus@gmail.com', 'somehashedpassword',
             '+2646173937494', '+26481048594', '', 'anaboom straat ERF 1037',
             'Dr Justus Voigt','938464933749','FNB Oshakati','60020','384793','Juschdus seine praxis','hcn 49384', 'super duber bester arzt','du alles so eigentlich')
