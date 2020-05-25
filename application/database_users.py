from application.db_utils import pool
from datetime import datetime

def checkUser(email):
    sql = """SELECT name, uuid_text, password FROM users WHERE email = '{}'
    """.format(email)
    conn = pool.connection()
    cursor = conn.cursor()
    cursor.execute(sql)
    data = cursor.fetchone()
    cursor.close()
    conn.close()
    return data


def checkDuplicateEmail(email):
    print(email)
    sql_check_duplicate = """SELECT * FROM users WHERE
    email='{}'""".format(email)
    conn = pool.connection()
    cursor = conn.cursor()
    cursor.execute(sql_check_duplicate)
    rows = cursor.fetchall()
    print(rows)
    if not rows:
        status = False
        print("no rows runs")
    else:
        status = True
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
    sql = """INSERT INTO users (uuid_bin, title, name, email, password, phone, cell, fax, address,
    bank_holder, bank_account, bank, bank_branch, practice_number, practice_name,
    hpcna_number, qualification, specialisation)
    VALUES(unhex(replace(uuid(),'-','')), '{0}','{1}','{2}','{3}','{4}','{5}','{6}','{7}','{8}','{9}','{10}','{11}','{12}','{13}','{14}','{15}','{16}')
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
    addUser("Dr", "Justus Voigt",'justus@gmail.com', 'somehashedpassword',
             '+2646173937494', '+26481048594', '', 'anaboom straat ERF 1037',
             'Dr Justus Voigt','938464933749','FNB Oshakati','60020','384793','Juschdus seine praxis','hcn 49384', 'super duber bester arzt','du alles so eigentlich')
