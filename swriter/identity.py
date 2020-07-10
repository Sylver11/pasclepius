from com.sun.star.text.ControlCharacter import PARAGRAPH_BREAK
from com.sun.star.style.ParagraphAdjust import CENTER, LEFT, RIGHT, BLOCK, STRETCH


def identityTable(doc, text, cursor, user, patient):
    top_table = doc.createInstance( "com.sun.star.text.TextTable" )
    top_table.initialize(1,2)
    top_table.setName('identity_table')
    text.insertTextContent( cursor, top_table, 1 )
    first_top_table_text = top_table.getCellByName("A1")
    first_top_table_text.setString("Practice No: " + user["practice_number"] +
                                   "\nHPCNA No: " + user["hpcna_number"] )
    cursor_top_right = top_table.createCursorByCellName("B1")
    cursor_top_right.setPropertyValue( "ParaAdjust", RIGHT )
    second_top_table_text = top_table.getCellByName("B1")
    if user['invoice_layout'] == 2 or user['invoice_layout'] == 5 or user['invoice_layout'] == 8 or user['invoice_layout'] == 11:
        second_top_table_text.setString(user["email"]
                + "\nCell: "
                + user["cell"]
                + "\nLandline: "
                + user["phone"])
    elif user['invoice_layout'] == 3 or user['invoice_layout'] == 6 or user['invoice_layout'] == 9 or user['invoice_layout'] == 12:
        second_top_table_text.setString(user["email"]
                + "\nCell: "
                + user["cell"]
                + "\nLandline: "
                + user["phone"]
                + "\nFax: "
                + user["fax"])
    else:
        second_top_table_text.setString(user["email"] + "\nCell: " + user["cell"])
    eText = top_table.getCellByName("B1").getText()
    eCursor = eText.createTextCursor()
    eText.insertString(eCursor, "", False)
    eCursor.goRight(len(user["email"]), True)
    eCursor.HyperLinkURL = "mailto:" + user["email"]
    range = top_table.getCellRangeByName("A1:B1")
    range.setPropertyValue( "CharFontName", "Liberation Serif" )
    range.setPropertyValue( "CharHeight", 10.0 )
    return doc, text, cursor

