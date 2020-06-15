from com.sun.star.style.ParagraphAdjust import CENTER, LEFT, RIGHT, BLOCK, STRETCH
from com.sun.star.text.ControlCharacter import PARAGRAPH_BREAK, APPEND_PARAGRAPH, LINE_BREAK
from com.sun.star.awt.FontWeight import BOLD as FW_BOLD


def hospitalTable(doc, text, cursor, patient):
    table = doc.createInstance( "com.sun.star.text.TextTable" )
    table.initialize(1,3)
    table.setName('hospital_table')
    text.insertTextContent( cursor, table, 1 )
    range = table.getCellRangeByName("A1:C1")
    range.setPropertyValue( "ParaAdjust", LEFT )
    range.setPropertyValue( "CharFontName", "Liberation Serif" )
    range.setPropertyValue( "CharHeight", 10.0 )
    range.setPropertyValue( "CharWeight", FW_BOLD)
    first_table_text = table.getCellByName("A1")
    first_table_text.setString("Hospital: " 
                + patient["hospital"])
    second_table_text = table.getCellByName("B1")
    second_table_text.setString("Date of Admission: "
                + patient['admission'])
    fourth_table_text = table.getCellByName("C1")
    fourth_table_text.setString("Date of Discharge: "
                + patient['discharge'])
    text.insertControlCharacter( cursor, PARAGRAPH_BREAK, False )
    return doc, text, cursor

