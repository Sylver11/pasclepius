from com.sun.star.style.ParagraphAdjust import CENTER, LEFT, RIGHT, BLOCK, STRETCH
from com.sun.star.text.ControlCharacter import PARAGRAPH_BREAK, APPEND_PARAGRAPH, LINE_BREAK
from com.sun.star.awt.FontWeight import BOLD as FW_BOLD, NORMAL

def diagnosisTable(doc, text, cursor, patient):
    table = doc.createInstance( "com.sun.star.text.TextTable" )
    table.initialize(3,2)
    table.ChartColumnAsLabel = False
    table.ChartRowAsLabel = False
    table.setName('diagnosis_table')
    text.insertTextContent( cursor, table, 1 )
    range = table.getCellRangeByName("A1:B3")
    range.setPropertyValue( "ParaAdjust", LEFT )
    range.setPropertyValue( "CharFontName", "Liberation Serif" )
    range.setPropertyValue( "CharHeight", 10.0 )
    range.setPropertyValue( "CharWeight", NORMAL)
    first_table_text = table.getCellByName("A1")
    first_table_text.setString("Diagnosis: "
                + patient["diagnosis"])
    second_table_text = table.getCellByName("B1")
    second_table_text.setString(patient['diagnosis_date'])
    third_table_text = table.getCellByName("A2")
    third_table_text.setString("Prodcedure: "
                + patient['procedure'])
    fourth_table_text = table.getCellByName("B2")
    fourth_table_text.setString(patient['procedure_date'])
    fifth_table_text = table.getCellByName("A3")
    fifth_table_text.setString("Implants: "
                + patient['implants'])

    sixth_table_text = table.getCellByName("B3")
    sixth_table_text.setString("Intra-OP Imaging: "
                + patient['intra-op']
                + "\nPost-OP Imaging: "
                + patient['post-op'])
    text.insertControlCharacter( cursor, PARAGRAPH_BREAK, False )
    return doc, text, cursor

