from db_utils import connection



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


def getTreatmentByItem(treatments):
  #  try:
    with connection.cursor() as cursor:
       # tupletreatments = tuple(treatments)
       # l=[]
        treatment_list=[]
        for i in treatments:
            print(i)
            sql = """SELECT description, units, value FROM treatments WHERE item = {}""".format(i)
            cursor.execute(sql)
            q = cursor.fetchone()
            treatment_list.append(q)
       # print(tupletreatments) 
      #  treatments.insert(0, 'item')
    # extratupletreatments = item + tupletreatments
       # item = tuple(treatments)
       # group_id = tuple(l)
       # print(item)
       # print(tupletreatments)
       # placeholder= '?' # For SQLite. See DBAPI paramstyle.
       # placeholders= ', '.join(placeholder for unused in treatments)
       # sql = """SELECT COUNT(*) AS total, description, units, value FROM treatments WHERE item IN {} ORDER BY FIELD{}""".format(tupletreatments, item) 
    #results = cursor.execute(sql)
       # sql = """SELECT description, units, value WHERE item IN {}""".format(tupletreatments)
       # print(tupletreatments)
       # cursor.execute(sql)
       # result = cursor.fetchall()
       # results = list(result)
        print(treatment_list)
       # for i in range(len(result)):
       #     print(result[i])
         #   return result
    #finally:
    #    connection.close()
       # return result

