from application.db_utils import pool
import os

def getAllTariffs():
    sql = """ SELECT tariff FROM namaf_tariffs GROUP BY tariff"""
    conn = pool.connection()
    cursor = conn.cursor()
    cursor.execute(sql)
    tariffs = cursor.fetchall()
    cursor.close()
    conn.close()
    return tariffs


def getValueTreatments(item, tariff):
    sql = """SELECT * FROM namaf_tariffs WHERE item = {} AND tariff = '{}'""".format(item, tariff)
    conn = pool.connection()
    cursor = conn.cursor()
    cursor.execute(sql)
    filtered_result = cursor.fetchone()
    cursor.close()
    conn.close()
    return filtered_result

def getMultipleValues(items, tariff):
    value_list=[]
    connection = pool.connection()
    cursor = connection.cursor()
    for i in items.split(","):
        sql = """SELECT description, value_cent FROM namaf_tariffs WHERE item = {} AND tariff = '{}'""".format(i, tariff)
        cursor.execute(sql)
        q = cursor.fetchone()
        value_list.append(q)
    cursor.close()
    connection.close()
    return value_list



def getTreatments(tariff, featured=None):
    if (featured is None):
        sql = """SELECT * FROM
        namaf_tariffs WHERE tariff = '{}' ORDER BY id""".format(tariff)
        connection = pool.connection()
        cursor = connection.cursor()
        cursor.execute(sql)
        filtered_result = cursor.fetchall()
        cursor.close()
        connection.close()
        return filtered_result

    elif(featured is not None):
        featured = tuple(featured)
        sql = """SELECT LPAD(item, 3, 0) AS item, description FROM
        namaf_tariffs WHERE item IN {} AND tariff = '{}' ORDER BY id""".format(featured, tariff)
        connection = pool.connection()
        cursor = connection.cursor()
        cursor.execute(sql)
        featured_result = cursor.fetchall()
        cursor.close()
        connection.close()
        return featured_result


def liveSearchTreatments(search, tariff):
    sql = """SELECT DISTINCT * FROM namaf_tariffs
    WHERE tariff = '{}' AND description LIKE '{}%'""".format(tariff, search)
    sql2 = """SELECT * FROM namaf_tariffs
    WHERE tariff = '{}' AND `procedure` LIKE '{}%'""".format(tariff, search)
    sql3 = """SELECT * FROM namaf_tariffs
    WHERE tariff = '{}' AND (category LIKE '%{}%'
    OR sub_category LIKE '%{}%' OR  sub_sub_category LIKE
    '%{}%')""".format(tariff, search, search, search)
    sql4 = """SELECT * FROM namaf_tariffs
    WHERE tariff = '{}' AND item LIKE '%{}%'""".format(tariff, search)
    connection = pool.connection()
    cursor = connection.cursor()
    cursor.execute(sql)
    result = cursor.fetchall()
    cursor.execute(sql2)
    result2 = cursor.fetchall()
    cursor.execute(sql3)
    result3 = cursor.fetchall()
    cursor.execute(sql4)
    result4 = cursor.fetchall()
    cursor.close()
    connection.close()
    return result, result2, result3, result4


def getTreatmentByGroup(items, tariff):
    treatment_list=[]
    connection = pool.connection()
    cursor = connection.cursor()
    for i in items.split(","):
        sql = """SELECT description FROM namaf_tariffs WHERE item = {} AND tariff = '{}'""".format(i, tariff)
        cursor.execute(sql)
        q = cursor.fetchone()
        treatment_list.append(q)
    cursor.close()
    connection.close()
    return treatment_list



def getTreatmentByItem(treatments, tariff):
    treatment_list=[]
    connection = pool.connection()
    cursor = connection.cursor()
    for i in treatments:
        sql = """SELECT description, units, value_cent FROM namaf_tariffs WHERE item = {} AND tariff = '{}'""".format(i, tariff)
        cursor.execute(sql)
        q = cursor.fetchone()
        treatment_list.append(q)
    cursor.close()
    connection.close()
    return treatment_list
