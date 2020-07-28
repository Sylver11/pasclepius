from application.db_utils import pool

def newWork(uuid_text, work_type, work_quality):
    conn = pool.connection()
    cursor = conn.cursor()
    if(work_type == 'invoice_tab'):
        sql_check_duplicate = """ SELECT * FROM user_workbench WHERE uuid_text
        = '{}' AND work_type = '{}' AND work_quality =
        '{}'""".format(uuid_text, work_type, work_quality)
        cursor.execute(sql_check_duplicate)
        row = cursor.fetchone()
        if(row):
            return 'success'
        sql_tab_count = """SELECT COUNT(*) FROM user_workbench WHERE uuid_text
        = '{}' AND work_type = 'invoice_tab'""".format(uuid_text)
        cursor.execute(sql_tab_count)
        rows = cursor.fetchone()
        if (rows['COUNT(*)'] > 4):
            num_to_delete = rows['COUNT(*)'] - 4
            sql_max_five = """DELETE FROM user_workbench WHERE uuid_text = '{}' AND
            work_type = 'invoice_tab' ORDER BY created_on DESC LIMIT
            {}""".format(uuid_text, num_to_delete)
            cursor.execute(sql_max_five)
    if(work_type == 'invoice_draft'):
        sql_delete_draft = """DELETE FROM user_workbench WHERE uuid_text = '{0}' AND
        work_type = 'invoice_draft'""".format(uuid_text)
        cursor.execute(sql_delete_draft)
    elif(work_type == 'patient_draft'):
        sql_delete_patient_draft =  """DELETE FROM user_workbench WHERE uuid_text = '{0}' AND
        work_type = 'patient_draft'""".format(uuid_text)
        cursor.execute(sql_delete_patient_draft)
    cursor.execute("""INSERT INTO user_workbench (uuid_text, work_type,
    work_quality) VALUES (%s, %s, %s)""",(uuid_text, work_type, work_quality))
    cursor.close()
    conn.close()
    return 'success'


def removeWork(uuid_text, work_type, work_quality):
    conn = pool.connection()
    cursor = conn.cursor()
    sql_delete = """DELETE FROM user_workbench WHERE uuid_text = '{0}' AND
        work_type = '{1}' AND work_quality = '{2}'""".format(uuid_text,
                work_type, work_quality)
    cursor.execute(sql_delete)
    cursor.close()
    conn.close()
    return 'success'


def lastFive(uuid_text, work_type):
    conn = pool.connection()
    cursor = conn.cursor()
    sql = """SELECT work_quality FROM user_workbench WHERE uuid_text = '{0}'
    AND work_type = '{1}' ORDER BY created_on DESC LIMIT 5""".format(uuid_text, work_type)
    cursor.execute(sql)
    last_five = cursor.fetchall()
    cursor.close()
    conn.close()
    return last_five
