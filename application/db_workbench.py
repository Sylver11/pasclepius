from application.db_utils import pool

def newWork(uuid_text, work_type, work_quality):
    conn = pool.connection()
    cursor = conn.cursor()
    sql_delete = """DELETE FROM user_workbench WHERE uuid_text = '{0}' AND
    work_type = '{1}' AND work_quality = '{2}'""".format(uuid_text, work_type, work_quality)
    cursor.execute(sql_delete)
    sql = """INSERT INTO user_workbench (uuid_text, work_type,
    work_quality) VALUES ('{0}', '{1}', '{2}')""".format(uuid_text, work_type, work_quality)
    cursor.execute(sql)
    cursor.close()
    conn.close()
    return 'success'
