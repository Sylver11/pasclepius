from com.sun.star.style.ParagraphAdjust import CENTER, LEFT, RIGHT, BLOCK, STRETCH
from com.sun.star.text.ControlCharacter import PARAGRAPH_BREAK, APPEND_PARAGRAPH, LINE_BREAK
from com.sun.star.awt.FontWeight import BOLD as FW_BOLD, NORMAL, LIGHT


def patientTable(doc, text, cursor, patient, invoice_id):
    cursor.setPropertyValue( "CharFontName", "Liberation Serif" )
    text.insertControlCharacter(cursor, PARAGRAPH_BREAK, False)
    cursor.setPropertyValue( "CharHeight", 12.0 )
    cursor.setPropertyValue( "ParaAdjust", RIGHT)
    text.insertString(cursor, patient['date_invoice'], 0)
    text.insertControlCharacter(cursor, PARAGRAPH_BREAK, False)
    cursor.setPropertyValue( "ParaAdjust", CENTER )
    cursor.setPropertyValue( "CharHeight", 18.0 )
    text.insertString( cursor, "Invoice", 0 )
    middle_table = doc.createInstance( "com.sun.star.text.TextTable" )
    if (patient['medical_aid'] == 'mva'):
        middle_table.initialize(2,3)
        middle_table.setName('patient_table')
        text.insertTextContent( cursor, middle_table, 1 )
        first_middle_table_text = middle_table.getCellByName("C2")
        first_middle_table_text.setString("Invoice No: " + str(invoice_id))
        second_middle_table_text = middle_table.getCellByName("A2")
        second_middle_table_text.setString("Patient Name: "
                + str(patient['patient_name'])
                + "\nPO: "
                + str(patient['po_number']))
        cursor_middle_right = middle_table.createCursorByCellName("C1")
        cursor_middle_right.setPropertyValue( "ParaAdjust", RIGHT )
        fourth_middle_table_text = middle_table.getCellByName("B2")
        fourth_middle_table_text.setString("Insurance: "
                + str(patient['medical_aid']).upper()
                + "\nCase Number: "
                + str(patient['case_number']))
        range = middle_table.getCellRangeByName("A1:C2")
        range.setPropertyValue( "CharFontName", "Liberation Serif" )
        range.setPropertyValue( "CharHeight", 10.0 )
        text.insertControlCharacter( cursor, PARAGRAPH_BREAK, False )

    else:
        middle_table.initialize(3,3)
        middle_table.setName('patient_table')
        text.insertTextContent( cursor, middle_table, 1 )
        first_middle_table_text = middle_table.getCellByName("C3")
        first_middle_table_text.setString("Invoice No: " + str(invoice_id))
        range_left = middle_table.getCellRangeByName("A1:A2")
        range_left.setPropertyValue( "ParaAdjust", LEFT )
        second_middle_table_text = middle_table.getCellByName("A2")
        second_middle_table_text.setString("Main Member: " + str(patient['main_member']))
        third_middle_table_text = middle_table.getCellByName("B2")
        third_middle_table_text.setString("Medical Aid No: " + str(patient['medical_number']))
        cursor_middle_right = middle_table.createCursorByCellName("C1")
        cursor_middle_right.setPropertyValue( "ParaAdjust", RIGHT )
        fourth_middle_table_text = middle_table.getCellByName("C2")
        fourth_middle_table_text.setString("Insurance: " + str(patient['medical_aid']).upper())
        fifth_middle_table_text = middle_table.getCellByName("A3")
        fifth_middle_table_text.setString("Patient Name: " + str(patient['patient_name']))
        sixth_middle_table_text = middle_table.getCellByName("B3")
        sixth_middle_table_text.setString("Patient DoB: " + str(patient['patient_birth_date']))
        range_bottom = middle_table.getCellRangeByName("A2:C3")
        range_bottom.setPropertyValue( "CharFontName", "Liberation Serif" )
        range_bottom.setPropertyValue( "CharHeight", 10.0 )
        range_top = middle_table.getCellRangeByName("A1:C1")
        range_top.setPropertyValue( "CharFontName", "Liberation Serif" )
        range_top.setPropertyValue( "CharHeight", 10.0 )
        text.insertControlCharacter( cursor, PARAGRAPH_BREAK, False )
    return doc, text, cursor

