from application.db_utils import pool

def newWork(uuid_text, practice_uuid, work_type, work_quality):
    conn = pool.connection()
    cursor = conn.cursor()
    if(work_type == 'invoice_tab'):
        sql_check_duplicate = """ SELECT * FROM user_workbench WHERE uuid_text
        = '{}' AND practice_uuid = '{}' AND work_type = '{}' AND work_quality =
        '{}'""".format(uuid_text, practice_uuid, work_type, work_quality)
        cursor.execute(sql_check_duplicate)
        row = cursor.fetchone()
        if(row):
            cursor.close()
            conn.close()
            return 'success'
        sql_tab_count = """SELECT COUNT(*) FROM user_workbench WHERE uuid_text
        = '{}' AND practice_uuid = '{}' AND work_type =
        'invoice_tab'""".format(uuid_text, practice_uuid)
        cursor.execute(sql_tab_count)
        rows = cursor.fetchone()
        if (rows['COUNT(*)'] > 2):
            num_to_delete = rows['COUNT(*)'] - 2
            sql_max_five = """DELETE FROM user_workbench WHERE uuid_text = '{}'
            AND practice_uuid = '{}' AND work_type = 'invoice_tab'
            ORDER BY created_on ASC LIMIT
            {}""".format(uuid_text, practice_uuid, num_to_delete)
            cursor.execute(sql_max_five)
    if(work_type == 'invoice_draft'):
        sql_delete_draft = """DELETE FROM user_workbench WHERE uuid_text =
        '{}' AND practice_uuid = '{}' AND work_type = 'invoice_draft'
        """.format(uuid_text, practice_uuid)
        cursor.execute(sql_delete_draft)
    elif(work_type == 'patient_draft'):
        sql_delete_patient_draft =  """DELETE FROM user_workbench WHERE uuid_text = '{}' AND
        practice_uuid = '{}' AND work_type = 'patient_draft'
        """.format(uuid_text, practice_uuid)
        cursor.execute(sql_delete_patient_draft)
    elif(work_type == 'patient_tab'):
        sql_delete_patient_tab =  """DELETE FROM user_workbench WHERE uuid_text = '{}' AND
        practice_uuid = '{}' AND work_type = 'patient_tab'""".format(uuid_text,
                practice_uuid)
        cursor.execute(sql_delete_patient_tab)
    cursor.execute("""INSERT INTO user_workbench (uuid_text, practice_uuid, work_type,
    work_quality) VALUES (%s, %s, %s, %s)""",(uuid_text, practice_uuid, work_type, work_quality))
    cursor.close()
    conn.close()
    return 'success'


def removeWork(uuid_text, practice_uuid, work_type, work_quality):
    conn = pool.connection()
    cursor = conn.cursor()
    sql = ''
    if work_type == 'invoice_draft':
        sql = """DELETE FROM user_workbench WHERE uuid_text = '{}' AND
        practice_uuid = '{}' AND work_type =
        'invoice_draft'""".format(uuid_text, practice_uuid)
    elif work_type == 'patient_tab':
        sql = """DELETE FROM user_workbench WHERE uuid_text = '{}' AND
        practice_uuid = '{}' AND work_type = 'patient_tab'""".format(uuid_text,
                practice_uuid)
    else:
        sql = """DELETE FROM user_workbench WHERE uuid_text = '{0}' AND
        practice_uuid = '{1}' AND work_type = '{2}' AND work_quality =
        '{3}'""".format(uuid_text, practice_uuid,
                work_type, work_quality)
    cursor.execute(sql)
    cursor.close()
    conn.close()
    return 'success'


def lastFive(uuid_text, practice_uuid, work_type):
    conn = pool.connection()
    cursor = conn.cursor()
    sql = """SELECT work_quality FROM user_workbench WHERE uuid_text = '{0}'
    AND practice_uuid = '{1}' AND work_type = '{2}' ORDER BY created_on DESC LIMIT
    5""".format(uuid_text, practice_uuid, work_type)
    cursor.execute(sql)
    last_five = cursor.fetchall()
    cursor.close()
    conn.close()
    return last_five
