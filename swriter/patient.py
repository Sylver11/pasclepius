from com.sun.star.style.ParagraphAdjust import CENTER, LEFT, RIGHT, BLOCK, STRETCH
from com.sun.star.text.ControlCharacter import PARAGRAPH_BREAK, APPEND_PARAGRAPH, LINE_BREAK
from com.sun.star.awt.FontWeight import BOLD as FW_BOLD, NORMAL, LIGHT


def patientTable(doc, text, cursor, patient, invoice_name, date_invoice):
    cursor.setPropertyValue( "CharFontName", "Liberation Serif" )
    text.insertControlCharacter(cursor, PARAGRAPH_BREAK, False)
    cursor.setPropertyValue( "CharHeight", 12.0 )
    cursor.setPropertyValue( "ParaAdjust", RIGHT)
    text.insertString(cursor, date_invoice[0], 0)
    text.insertControlCharacter(cursor, PARAGRAPH_BREAK, False)
    cursor.setPropertyValue( "ParaAdjust", CENTER )
    cursor.setPropertyValue( "CharHeight", 18.0 )
    text.insertString( cursor, "Invoice", 0 )
    middle_table = doc.createInstance( "com.sun.star.text.TextTable" )
    if (patient['medical'] == 'mva'):
        middle_table.initialize(2,3)
        middle_table.setName('patient_table')
        text.insertTextContent( cursor, middle_table, 1 )
        first_middle_table_text = middle_table.getCellByName("C2")
        first_middle_table_text.setString("Invoice No: " + str(invoice_name))
        second_middle_table_text = middle_table.getCellByName("A2")
        second_middle_table_text.setString("Patient Name: "
                + str(patient['name'])
                + "\nPO: "
                + str(patient['po']))
        cursor_middle_right = middle_table.createCursorByCellName("C1")
        cursor_middle_right.setPropertyValue( "ParaAdjust", RIGHT )
        fourth_middle_table_text = middle_table.getCellByName("B2")
        fourth_middle_table_text.setString("Insurance: "
                + str(patient['medical']).upper()
                + "\nCase Number: "
                + str(patient['case']))
        range = middle_table.getCellRangeByName("A1:C2")
        range.setPropertyValue( "CharFontName", "Liberation Serif" )
        range.setPropertyValue( "CharHeight", 10.0 )
        text.insertControlCharacter( cursor, PARAGRAPH_BREAK, False )

    else:
        middle_table.initialize(3,3)
        middle_table.setName('patient_table')
        text.insertTextContent( cursor, middle_table, 1 )
        first_middle_table_text = middle_table.getCellByName("C3")
        first_middle_table_text.setString("Invoice No: " + str(invoice_name))
       # first_middle_table_text.setPropertyValue( "CharFontName", "Liberation Serif" )
       # first_middle_table_text.setPropertyValue( "CharHeight", 10.0 )
        range_left = middle_table.getCellRangeByName("A1:A2")
        range_left.setPropertyValue( "ParaAdjust", LEFT )
        second_middle_table_text = middle_table.getCellByName("A2")
        second_middle_table_text.setString("Main Member: " + str(patient['main']))
        third_middle_table_text = middle_table.getCellByName("B2")
        third_middle_table_text.setString("Medical Aid No: " + str(patient['number']))
        cursor_middle_right = middle_table.createCursorByCellName("C1")
        cursor_middle_right.setPropertyValue( "ParaAdjust", RIGHT )
       # cursor_middle_table_c1 = middle_table.getCellByName("C1")
       # cursor_middle_table_c1.setString("Date: " + date_invoice[0])
        fourth_middle_table_text = middle_table.getCellByName("C2")
        fourth_middle_table_text.setString("Insurance: " + str(patient['medical']).upper())
        fifth_middle_table_text = middle_table.getCellByName("A3")
        fifth_middle_table_text.setString("Patient Name: " + str(patient['name']))
        sixth_middle_table_text = middle_table.getCellByName("B3")
        sixth_middle_table_text.setString("Patient DoB: " + str(patient['dob']))
       # seventh_middle_table_text = middle_table.getCellByName("B1")
       # seventh_middle_table_text.setString("Invoice")
        range_bottom = middle_table.getCellRangeByName("A2:C3")
        range_bottom.setPropertyValue( "CharFontName", "Liberation Serif" )
        range_bottom.setPropertyValue( "CharHeight", 10.0 )
       # seventh_middle_table_text.setPropertyValue("CharHeight", 18)
       # seventh_middle_table_text.setPropertyValue("CharWeight", LIGHT)
       # range_xx = middle_table.getCellRangeByName("A1:C1")
       # range_xx.setPropertyValue("CharWeight", NORMAL)
       # range_xx.setPropertyValue( "ParaAdjust", CENTER )

        range_top = middle_table.getCellRangeByName("A1:C1")
        range_top.setPropertyValue( "CharFontName", "Liberation Serif" )
        range_top.setPropertyValue( "CharHeight", 10.0 )
        text.insertControlCharacter( cursor, PARAGRAPH_BREAK, False )
    return doc, text, cursor

