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

try:
    with connection.cursor() as cursor:

  #      sql = """INSERT INTO treatments (item, description, units, value,category, year) VALUES (%s, %s, %s, %s, %s, %s)"""
        cursor.execute(sql)
   #     cursor.executemany(sql, [('001', 'Infra-red, Radiant heat, Wax therapy Hot packs', '10.00', '98.40','RADIATION THERAPY / MOIST HEAT / CRYOTHERAPY', '2019'), ('005', 'Ultraviolet light', '17.00', '167.20','RADIATION THERAPY / MOIST HEAT / CRYOTHERAPY', '2019'),('006','Laser beam', '17.00', '167.20', 'RADIATION THERAPY / MOIST HEAT / CRYOTHERAPY', '2019')])

    connection.commit()

   # with connection.cursor() as cursor:
        # Read a single record
 #       sql = """SELECT id, LPAD(item, 3, 0) AS item, description,FORMAT(units,2) AS units, value, category, year FROM treatments"""
 #       cursor.execute(sql)
 #       result = cursor.fetchall()
 #       print(result)
finally:
    connection.close()
