from application.db_utils import pool

def newWork(uuid_text, work_type, work_quality):
    conn = pool.connection()
    cursor = conn.cursor()
    cursor.execute(""""INSERT INTO usr_workbench (uuid_text, work_type,
    work_quality) VALUE ('{0}', '{1}', '{2}')""".format(uuid_text, work_type, work_quality))
    cursor.close()
    conn.close()
    return 'success'
