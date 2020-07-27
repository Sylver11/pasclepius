from application.db_utils import pool

def newWork(uuid_text, work_type, work_quality):
    conn = pool.connection()
    cursor = conn.cursor()
    sql_delete_draft = """DELETE FROM user_workbench WHERE uuid_text = '{0}' AND
    work_type = 'invoice_draft'""".format(uuid_text)
   # cursor.execute(sql_delete_draft)
    sql_delete = """DELETE FROM user_workbench WHERE uuid_text = '{0}' AND
    work_type = '{1}' AND work_quality = '{2}'""".format(uuid_text, work_type, work_quality)
    cursor.execute(sql_delete)
    sql = """INSERT INTO user_workbench (uuid_text, work_type,
    work_quality) VALUES ('{0}', '{1}', '{2}')""".format(uuid_text, work_type, work_quality)
    cursor.execute(sql)
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
