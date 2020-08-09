from application.db_utils import pool
from datetime import datetime

def checkDuplicate(uuid, patient):
    sql = """SELECT * FROM patients WHERE uuid_text = '{}' AND
    (medical_number = '{}' OR case_number = '{}')
    """.format(uuid, patient.get('medical_number'),
            patient.get('case_number'))
    conn = pool.connection()
    cursor = conn.cursor()
    cursor.execute(sql)
    row = cursor.fetchone()
    cursor.close()
    conn.close()
    return row


def patientSearch(uuid, patient_name):
    sql = """SELECT 
    any_value(patients.patient_id) AS patient_id,
    any_value(patients.patient_name) AS patient_name,
    any_value(patients.medical_aid) AS medical_aid,
    any_value(patients.main_member) AS main_member,
    any_value(patients.patient_birth_date) AS patient_birth_date,
    any_value(patients.medical_number) AS medical_number,
    any_value(patients.case_number) AS case_number,
    any_value(patients.patient_note) AS patient_note,
    any_value(patients.created_on) AS created_on
    FROM patients WHERE uuid_text = '{}' AND patient_name LIKE '%{}%'
    GROUP BY medical_number, case_number
    """.format(uuid, patient_name)
    conn = pool.connection()
    cursor = conn.cursor()
    cursor.execute(sql)
    patients = cursor.fetchall()
    cursor.close()
    conn.close()
    return patients


def insertPatient(uuid_text, patient):
    conn = pool.connection()
    cursor = conn.cursor()
    cursor.execute("""INSERT INTO patients (uuid_text, patient_name,
    medical_aid, main_member, patient_birth_date, medical_number,
    case_number, patient_note) VALUES(%s, %s, %s, %s, %s, %s, %s, %s)""",
    (uuid_text,
            patient.get('patient_name'),
            patient.get('medical_aid'),
            patient.get('main_member'),
            patient.get('patient_birth_date') or None,
            patient.get('medical_number'),
            patient.get('case_number'),
            patient.get('patient_note')))

    cursor.close()
    conn.close()
