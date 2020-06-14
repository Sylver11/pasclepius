from com.sun.star.text.ControlCharacter import PARAGRAPH_BREAK
from com.sun.star.style.ParagraphAdjust import CENTER, LEFT, RIGHT, BLOCK, STRETCH


def identityTable(doc, text, cursor, patient, data):
    top_table = doc.createInstance( "com.sun.star.text.TextTable" )
    top_table.initialize(1,2)
    top_table.setName('top_Table')
    text.insertTextContent( cursor, top_table, 1 )
    first_top_table_text = top_table.getCellByName("A1")
    first_top_table_text.setString("Practice No: " + data["practice_number"] +
                                   "\nHPCNA No: " + data["hpcna_number"] )
    cursor_top_right = top_table.createCursorByCellName("B1")
    cursor_top_right.setPropertyValue( "ParaAdjust", RIGHT )
    second_top_table_text = top_table.getCellByName("B1")
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

