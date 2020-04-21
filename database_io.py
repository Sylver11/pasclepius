from db_utils import pool
from swriter import createTextInvoice

def setupTable():
    sql = """CREATE TABLE treatments (
    id int(11) NOT NULL AUTO_INCREMENT,
    item int(11) NOT NULL,
    description varchar(255) COLLATE utf8_bin NOT NULL,
    units int(11) NOT NULL,
    value decimal(10,2) NOT NULL,
    category varchar(255) COLLATE utf8_bin NOT NULL,
    tariff varchar(255) NOT NULL,
    PRIMARY KEY (id)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin
    AUTO_INCREMENT=1 ;"""
    try:
        with connection.cursor() as cursor:
            cursor.execute(sql)
    finally:
        connection.close()
#setupTable()
#mysqlimport --ignore-lines=1 --fields-terminated-by=\; --columns='item,description,units,value,category,tariff' --local -u root -p pasclepius /Users/justusvoigt/Documents/treatments.csv

def getValueTreatments(item, tariff):
    sql = """SELECT value FROM treatments WHERE item = {} AND tariff = '{}'""".format(item, tariff)
    conn = pool.connection()
    cursor = conn.cursor()
    cursor.execute(sql)
    filtered_result = cursor.fetchone()
    cursor.close()
    conn.close()
    return filtered_result 

def getTreatments(tariff, featured=None):
    if (featured is None):
        sql = """SELECT LPAD(item, 3, 0) AS item, description, category FROM treatments WHERE tariff = '{}' ORDER BY id""".format(tariff)
        connection = pool.connection()
        cursor = connection.cursor()
        cursor.execute(sql)
        filtered_result = cursor.fetchall()
        cursor.close()
        connection.close()
        return filtered_result

    elif(featured is not None):
        featured = tuple(featured)
        sql = """SELECT LPAD(item, 3, 0) AS item, description FROM treatments WHERE item IN {} AND tariff = '{}' ORDER BY id""".format(featured, tariff)
        connection = pool.connection()
        cursor = connection.cursor()
        cursor.execute(sql)
        featured_result = cursor.fetchall()
        cursor.close()
        connection.close()
        return featured_result


def getTreatmentByItem(treatments, tariff, value, dates, patient, modifier):
    treatment_list=[]
    connection = pool.connection()
    cursor = connection.cursor()
    for i in treatments:
        sql = """SELECT description, units, value FROM treatments WHERE item = {} AND tariff = '{}'""".format(i, tariff)
        cursor.execute(sql)
        q = cursor.fetchone()
        treatment_list.append(q)
    createTextInvoice(treatments, treatment_list, value,  dates, patient, modifier)
    cursor.close()
    connection.close()
