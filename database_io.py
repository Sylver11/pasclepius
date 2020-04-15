from db_utils import connection
from swriter import populateTable, setupConnection


#sql = """CREATE TABLE treatments (
#    id int(11) NOT NULL AUTO_INCREMENT,
#    item int(11) NOT NULL,
#    description varchar(255) COLLATE utf8_bin NOT NULL,
#    units int(11) NOT NULL,
#    value decimal(10,2) NOT NULL,
#    category varchar(255) COLLATE utf8_bin NOT NULL,
#    year int(11) NOT NULL,
#    PRIMARY KEY (id)
#) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin
#AUTO_INCREMENT=1 ;"""


#mysqlimport --ignore-lines=1 --fields-terminated-by=\; --columns='item,description,units,value,category,year' --local -u root -p pasclepius /Users/justusvoigt/Documents/treatments.csv



def getTreatments2019():
   # try:
    with connection.cursor() as cursor:
        sql = """SELECT LPAD(item, 3, 0) AS item, description FROM treatments ORDER BY id"""
        cursor.execute(sql)
        filtered_result = cursor.fetchall()
           # return filtered_result
   # finall:
   #     connection.close()
        return filtered_result


def getTreatmentByItem(treatments, dates, patient):
  #  try:
    with connection.cursor() as cursor:
        treatment_list=[]
        for i in treatments:
            sql = """SELECT description, units, value FROM treatments WHERE item = {}""".format(i)
            cursor.execute(sql)
            q = cursor.fetchone()
            #print(q['value'])
            #print(q)
            treatment_list.append(q)
        setupConnection()
        populateTable(treatments, treatment_list, dates, patient)
