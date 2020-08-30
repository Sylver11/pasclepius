from com.sun.star.style.ParagraphAdjust import CENTER, LEFT, RIGHT, BLOCK, STRETCH
from com.sun.star.text.ControlCharacter import PARAGRAPH_BREAK, APPEND_PARAGRAPH, LINE_BREAK
from com.sun.star.awt.FontWeight import BOLD as FW_BOLD


def hospitalTable(doc, text, cursor, patient):
    table = doc.createInstance( "com.sun.star.text.TextTable" )
    table.initialize(1,6)
    table.setName('hospital_table')
    text.insertTextContent( cursor, table, 1 )
    range = table.getCellRangeByName("A1:F1")
    range.setPropertyValue( "ParaAdjust", LEFT )
    range.setPropertyValue( "CharFontName", "Liberation Serif" )
    range.setPropertyValue( "CharHeight", 10.0 )
    first_table_text = table.getCellByName("A1")
    first_table_text.setString("Hospital:")
   # first_table_text.setPropertyValue( "CharWeight", FW_BOLD)
    first_first = table.getCellByName("B1")
    first_first.setString(patient["hospital_name"])
    second_table_text = table.getCellByName("C1")
    second_table_text.setString("Date of Admission:")
   # second_table_text.setPropertyValue( "CharWeight", FW_BOLD)
    second_second = table.getCellByName("D1")
    second_second.setString( patient['admission_date'])
    fourth_table_text = table.getCellByName("E1")
    fourth_table_text.setString("Date of Discharge:")
   # fourth_table_text.setPropertyValue( "CharWeight", FW_BOLD)
    fourth_fourth = table.getCellByName("F1")
    fourth_fourth.setString(patient['discharge_date'])
    text.insertControlCharacter( cursor, PARAGRAPH_BREAK, False )
    return doc, text, cursor

