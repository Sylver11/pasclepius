from application.db_utils import pool
from datetime import datetime

def checkDuplicate(practice_uuid, patient):
    sql = """SELECT * FROM patients WHERE practice_uuid = '{}' AND
    (medical_number = '{}' OR case_number = '{}' OR medical_number = '{}' OR case_number = '{}')
    """.format(practice_uuid,
            patient.get('medical_number'),
            patient.get('case_number'),
            patient.get('case_number'),
            patient.get('medical_number'))
    conn = pool.connection()
    cursor = conn.cursor()
    cursor.execute(sql)
    row = cursor.fetchone()
    cursor.close()
    conn.close()
    return row


def patientSearch(practice_uuid, patient_name):
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
    FROM patients WHERE practice_uuid = '{}' AND patient_name LIKE '%{}%'
    GROUP BY patients.medical_number, patients.case_number
    """.format(practice_uuid, patient_name)
    conn = pool.connection()
    cursor = conn.cursor()
    cursor.execute(sql)
    patients = cursor.fetchall()
    cursor.close()
    conn.close()
    return patients

def removePatient(practice_uuid, patient_id):
    conn = pool.connection()
    cursor = conn.cursor()
    sql = """ DELETE FROM patients WHERE practice_uuid = '{}' AND
    patient_id = '{}'""".format(practice_uuid, patient_id)
    cursor.execute(sql)
    cursor.close()
    conn.close()
    status = True
    return status


def insertPatient(practice_uuid, patient):
    conn = pool.connection()
    cursor = conn.cursor()
    cursor.execute("""INSERT INTO patients (practice_uuid, patient_name,
    medical_aid, main_member, patient_birth_date, medical_number,
    case_number, patient_note) VALUES(%s, %s, %s, %s, %s, %s, %s, %s)""",
    (practice_uuid,
            patient.get('patient_name'),
            patient.get('medical_aid'),
            patient.get('main_member'),
            patient.get('patient_birth_date') or None,
            patient.get('medical_number'),
            patient.get('case_number'),
            patient.get('patient_note')))

    cursor.close()
    conn.close()
