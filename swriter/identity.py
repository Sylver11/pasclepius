from com.sun.star.text.ControlCharacter import PARAGRAPH_BREAK
from com.sun.star.style.ParagraphAdjust import CENTER, LEFT, RIGHT, BLOCK, STRETCH


def identityTable(doc, text, cursor, layout, patient, data):
    top_table = doc.createInstance( "com.sun.star.text.TextTable" )
    top_table.initialize(1,2)
    top_table.setName('identity_table')
    text.insertTextContent( cursor, top_table, 1 )
    first_top_table_text = top_table.getCellByName("A1")
    first_top_table_text.setString("Practice No: " + data["practice_number"] +
                                   "\nHPCNA No: " + data["hpcna_number"] )
    cursor_top_right = top_table.createCursorByCellName("B1")
    cursor_top_right.setPropertyValue( "ParaAdjust", RIGHT )
    second_top_table_text = top_table.getCellByName("B1")
    if layout == 2 or layout == 5 or layout == 8 or layout == 11:
        second_top_table_text.setString(data["email"]
                + "\nCell: "
                + data["cell"]
                + "\nLandline: "
                + data["phone"])
    elif layout == 3 or layout == 6 or layout == 9 or layout == 12:
        second_top_table_text.setString(data["email"]
                + "\nCell: "
                + data["cell"]
                + "\nLandline: "
                + data["phone"]
                + "\nFax: "
                + data["fax"])
    else:
        second_top_table_text.setString(data["email"] + "\nCell: " + data["cell"])
    eText = top_table.getCellByName("B1").getText()
    eCursor = eText.createTextCursor()
    eText.insertString(eCursor, "", False)
    eCursor.goRight(len(data["email"]), True)
    eCursor.HyperLinkURL = "mailto:" + data["email"]
    range = top_table.getCellRangeByName("A1:B1")
    range.setPropertyValue( "CharFontName", "Liberation Serif" )
    range.setPropertyValue( "CharHeight", 10.0 )
    text.insertControlCharacter( cursor, PARAGRAPH_BREAK, False );
    return doc, text, cursor

