from com.sun.star.style.ParagraphAdjust import CENTER, LEFT, RIGHT, BLOCK, STRETCH
from com.sun.star.text.ControlCharacter import PARAGRAPH_BREAK, APPEND_PARAGRAPH, LINE_BREAK


def populateTopText(cursor, doc, text, data):
    #global cursor
   # cursor = text.createTextCursor()
    cursor.setPropertyValue( "CharFontName", "Liberation Serif" )
    cursor.setPropertyValue( "CharHeight", 10.0 )
    cursor.setPropertyValue( "ParaAdjust", CENTER )
    text.insertString( cursor, data["practice_name"], 0 )
    text.insertControlCharacter( cursor, PARAGRAPH_BREAK, False )
    text.insertString( cursor, data["qualification"], 0 )
    text.insertControlCharacter( cursor, PARAGRAPH_BREAK, False )
    text.insertControlCharacter( cursor, PARAGRAPH_BREAK, False )
    text.insertControlCharacter( cursor, PARAGRAPH_BREAK, False )
    return doc, text, cursor
