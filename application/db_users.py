from application.db_utils import pool


def removeEntry(_sIdentifier, _sColumn, _sTable):
    try:
        conn = pool.connection()
        cursor = conn.cursor()
        cursor.execute("""DELETE FROM %s WHERE %s = %s""",(_sTable, _sColumn,
            _sTable))
    except:
        return False
    return True


def getScalar( _sIdentifier, _sLkpVal, _sLkpCol, _sLkpTbl, _sOrderBy = None):
    try:
        conn = pool.connection()
        cursor = conn.cursor()
        sql = 'SELECT ' + _sIdentifier + ' FROM ' + _sLkpTbl
        sql += ' WHERE ' + _sLkpCol + ' = %s '
        if _sOrderBy:
            sql += ' ORDER BY ' + _sOrderBy + ' DESC '
        cursor.execute(sql,( _sLkpVal ))
        _sScalar = cursor.fetchone()
        cursor.close()
        conn.close()
    except  Exception as e:
        return str(e)
    return _sScalar


def updateScalar( _sVal, _sCol, _sIdentifier, _sLkpCol, _sLkpTbl):
    try:
        conn = pool.connection()
        cursor = conn.cursor()
        sql = 'UPDATE ' + _sLkpTbl
        sql += ' SET ' + _sCol + '=%s WHERE ' + _sLkpCol + '= %s'
        cursor.execute(sql, ( _sVal, _sIdentifier))
        cursor.close()
        conn.close()
    except Exception as e:
        print(str(e))
        return False
    return True


def checkUser(email):
    conn = pool.connection()
    cursor = conn.cursor()
    cursor.execute("""SELECT * FROM users WHERE email =  %s""",(email))
    data = cursor.fetchone()
    cursor.close()
    conn.close()
    return data


def updateInvoice(practice_uuid, phone, fax, hospital, diagnosis):
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
    sql = """UPDATE practices SET invoice_layout = '{}' WHERE
    practice_uuid = '{}'""".format(layout_code, practice_uuid)
    conn = pool.connection()
    cursor = conn.cursor()
    cursor.execute(sql)
    cursor.close()
    conn.close()
    status = True
    return status



def updatePractice(practice_uuid, practice_form):
    conn = pool.connection()
    cursor = conn.cursor()
    cursor.execute(""" UPDATE practices SET 
    practice_email = %s,
    phone = %s,
    cell = %s,
    fax = %s,
    pob = %s,
    city = %s,
    country = %s,
    bank_holder = %s,
    bank_account = %s,
    bank = %s,
    bank_branch = %s,
    practice_number = %s,
    practice_name = %s,
    hpcna_number = %s,
    qualification = %s,
    specialisation = %s,
    namaf_profession = %s  WHERE practice_uuid = %s
    """,(practice_form.get('practice_email'),
            practice_form.get('phone'),
            practice_form.get('cell'),
            practice_form.get('fax'),
            practice_form.get('pob'),
            practice_form.get('city'),
            practice_form.get('country'),
            practice_form.get('bank_holder'),
            practice_form.get('bank_account'),
            practice_form.get('bank'),
            practice_form.get('bank_branch'),
            practice_form.get('practice_number'),
            practice_form.get('practice_name'),
            practice_form.get('hpcna_number'),
            practice_form.get('qualification'),
            practice_form.get('specialisation'),
            practice_form.get('namaf_profession'),
            practice_uuid))
    cursor.close()
    conn.close()
    status = True
    return status



def updateUser(email, first_name = '', second_name = '', current_practice_uuid = '',
        current_practice_role = ''):
    sql = ''
    if(current_practice_uuid):
        sql = """UPDATE users SET current_practice_uuid = '{}',
        current_practice_role = '{}' WHERE
        email = '{}'""".format(current_practice_uuid, current_practice_role, email)
    else:
        sql = """UPDATE users SET first_name = '{}', second_name = '{}' WHERE
        email = '{}'""".format(first_name, second_name, email)
    conn = pool.connection()
    cursor = conn.cursor()
    cursor.execute(sql)
    cursor.close()
    conn.close()
    status = True
    return status



def addUser(first_name, second_name, email):
    conn = pool.connection()
    cursor = conn.cursor()
    cursor.execute("""INSERT INTO users (uuid_bin, first_name, second_name, email)
    VALUES(unhex(replace(uuid(),'-','')),%s,%s,%s)
    """,(first_name, second_name, email))
    status = True
    cursor.close()
    conn.close()
    return status



def getPractice(practice_admin = '', practice_uuid = ''):
    conn = pool.connection()
    cursor = conn.cursor()
    sql = ''
    if practice_admin:
        sql = """SELECT * FROM practices WHERE practice_admin =
        '{}'""".format(practice_admin)
    else:
        sql = """ SELECT * FROM practices WHERE practice_uuid =
        '{}'""".format(practice_uuid)

    cursor.execute(sql)
    practice = cursor.fetchone()
    cursor.close()
    conn.close()
    return practice


def mergeUserPractice(practice_uuid, practice_name, user_uuid, user_email,
        user_name, role):
    try:
        conn = pool.connection()
        cursor = conn.cursor()
        sql = """UPDATE users SET current_practice_uuid = '{}', current_practice_role = '{}' WHERE uuid_text = '{}'""".format(practice_uuid, role, user_uuid)
        cursor.execute(sql)
        cursor.execute("""SELECT * FROM practice_connections WHERE practice_uuid = %s AND user_uuid = %s""",(practice_uuid, user_uuid))
        row = cursor.fetchone()
        if not row:
            cursor.execute("""INSERT INTO practice_connections
            (practice_uuid, practice_name,
            user_uuid, user_email, user_name, practice_role)
            VALUES(%s,%s,%s,%s,%s,%s)""",(practice_uuid,
            practice_name, user_uuid, user_email, user_name, role))
        cursor.close()
        conn.close()
    except Exception as e:
        app.logger.info(str(e)) 
        return False
    return True


def getAssistants(practice_uuid):
    conn = pool.connection()
    cursor = conn.cursor()
    sql = """SELECT * FROM practice_connections WHERE practice_uuid =
    '{}' AND practice_role = 'assistant'""".format(practice_uuid)
    cursor.execute(sql)
    assistants = cursor.fetchall()
    cursor.close()
    conn.close()
    return assistants


def checkConnections(user_uuid):
    conn = pool.connection()
    cursor = conn.cursor()
    sql = """SELECT * FROM practice_connections WHERE user_uuid =
    '{}'""".format(user_uuid)
    cursor.execute(sql)
    practices = cursor.fetchall()
    cursor.close()
    conn.close()
    return practices


def addPractice(email, practice_form):
    conn = pool.connection()
    cursor = conn.cursor()
    cursor.execute("""INSERT INTO practices (uuid_bin, practice_admin,
        practice_email, phone,
        cell, fax, pob, city, country,
        bank_holder, bank_account, bank,
        bank_branch, practice_number, practice_name,
        hpcna_number, qualification, specialisation,
        namaf_profession)
        VALUES(unhex(replace(uuid(),'-','')),%s,%s,%s,%s,
        %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
        """,(email,
            practice_form.get('practice_email'),
            practice_form.get('phone'),
            practice_form.get('cell'),
            practice_form.get('fax'),
            practice_form.get('pob'),
            practice_form.get('city'),
            practice_form.get('country'),
            practice_form.get('bank_holder'),
            practice_form.get('bank_account'),
            practice_form.get('bank'),
            practice_form.get('bank_branch'),
            practice_form.get('practice_number'),
            practice_form.get('practice_name'),
            practice_form.get('hpcna_number'),
            practice_form.get('qualification'),
            practice_form.get('specialisation'),
            practice_form.get('namaf_profession')))
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
