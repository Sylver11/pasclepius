from com.sun.star.style.ParagraphAdjust import CENTER, LEFT, RIGHT, BLOCK, STRETCH
from com.sun.star.text.ControlCharacter import PARAGRAPH_BREAK, APPEND_PARAGRAPH, LINE_BREAK
from com.sun.star.awt.FontWeight import BOLD as FW_BOLD, NORMAL

def diagnosisTable(doc, text, cursor, patient):
    table = doc.createInstance( "com.sun.star.text.TextTable" )
    table.initialize(3,4)
    table.ChartColumnAsLabel = False
    table.ChartRowAsLabel = False
    table.setName('diagnosis_table')
    text.insertTextContent( cursor, table, 1 )
    range = table.getCellRangeByName("A1:D3")
    range.setPropertyValue( "ParaAdjust", LEFT )
    range.setPropertyValue( "CharFontName", "Liberation Serif" )
    range.setPropertyValue( "CharHeight", 10.0 )
    range_x = table.getCellRangeByName("B1:D1")
    range_x.setPropertyValue( "CharWeight", NORMAL)
    first_table_text = table.getCellByName("A1")
    first_table_text.setString("Diagnosis:")
    first_table_text.setPropertyValue( "CharWeight", FW_BOLD)
    first_first = table.getCellByName("B1")
    first_first.setString(patient["diagnosis"])
    second_table_text = table.getCellByName("D1")
    second_table_text.setString(patient['diagnosis_date'])
    third_table_text = table.getCellByName("A2")
    third_table_text.setString("Procedure:")
    third_table_text.setPropertyValue( "CharWeight", FW_BOLD)
    third_third = table.getCellByName("B2")
    third_third.setString(patient['procedure'])
    fourth_table_text = table.getCellByName("D2")
    fourth_table_text.setString(patient['procedure_date'])
    fifth_table_text = table.getCellByName("A3")
    fifth_table_text.setString("Implants:")
    fifth_table_text.setPropertyValue( "CharWeight", FW_BOLD)
    fifth_fifth = table.getCellByName("B3")
    fifth_fifth.setString(patient['implants'])
    sixth_table_text = table.getCellByName("C3")
    sixth_table_text.setString("Intra-OP Imaging\nPost-OP Imaging")
    sixth_table_text.setPropertyValue( "CharWeight", FW_BOLD)
    sixth_sixth = table.getCellByName("D3")
    sixth_sixth.setString(patient['intra-op']
                + "\n"
                + patient['post-op'])
    text.insertControlCharacter( cursor, PARAGRAPH_BREAK, False )
    return doc, text, cursor

