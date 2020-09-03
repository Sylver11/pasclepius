from com.sun.star.text.ControlCharacter import PARAGRAPH_BREAK
from com.sun.star.style.ParagraphAdjust import CENTER, LEFT, RIGHT, BLOCK, STRETCH


def identityTable(doc, text, cursor, practice, patient):
    top_table = doc.createInstance( "com.sun.star.text.TextTable" )
    top_table.initialize(1,2)
    top_table.setName('identity_table')
    text.insertTextContent( cursor, top_table, 1 )
    first_top_table_text = top_table.getCellByName("A1")
    first_top_table_text.setString("Practice No: " + practice["practice_number"] +
                                   "\nHPCNA No: " + practice["hpcna_number"] )
    cursor_top_right = top_table.createCursorByCellName("B1")
    cursor_top_right.setPropertyValue( "ParaAdjust", RIGHT )
    second_top_table_text = top_table.getCellByName("B1")
    if practice['invoice_layout'] == 2 or practice['invoice_layout'] == 5 or practice['invoice_layout'] == 8 or practice['invoice_layout'] == 11:
        second_top_table_text.setString(practice["practice_email"]
                + "\nCell: "
                + practice["cell"]
                + "\nLandline: "
                + practice["phone"])
    elif practice['invoice_layout'] == 3 or practice['invoice_layout'] == 6 or practice['invoice_layout'] == 9 or practice['invoice_layout'] == 12:
        second_top_table_text.setString(practice["practice_email"]
                + "\nCell: "
                + practice["cell"]
                + "\nLandline: "
                + practice["phone"]
                + "\nFax: "
                + practice["fax"])
    else:
        second_top_table_text.setString(practice["practice_email"] + "\nCell: "
                + practice["cell"])
    eText = top_table.getCellByName("B1").getText()
    eCursor = eText.createTextCursor()
    eText.insertString(eCursor, "", False)
    eCursor.goRight(len(practice["practice_email"]), True)
    eCursor.HyperLinkURL = "mailto:" + practice["practice_email"]
    range = top_table.getCellRangeByName("A1:B1")
    range.setPropertyValue( "CharFontName", "Liberation Serif" )
    range.setPropertyValue( "CharHeight", 10.0 )
    return doc, text, cursor

