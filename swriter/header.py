from com.sun.star.style.ParagraphAdjust import CENTER, LEFT, RIGHT, BLOCK, STRETCH
from com.sun.star.text.ControlCharacter import PARAGRAPH_BREAK, APPEND_PARAGRAPH, LINE_BREAK


def populateTopText(cursor, doc, text, data):
    styles = doc.StyleFamilies
    page_styles = styles.getByName("PageStyles")
    oDefaultStyle = page_styles.getByName("Standard")
    oDefaultStyle.HeaderIsOn = True
    header_text = oDefaultStyle.getPropertyValue("HeaderText")
    header_cursor = header_text.createTextCursor()
    header_cursor.setPropertyValue( "CharFontName", "Liberation Serif" )
    header_cursor.setPropertyValue( "CharHeight", 18.0 )
    header_cursor.setPropertyValue( "ParaAdjust", CENTER )
    header_text.insertString(header_cursor, data["practice_name"], 0)
    header_text.insertControlCharacter( header_cursor, PARAGRAPH_BREAK, False )
    header_cursor.setPropertyValue( "CharHeight", 12.0 )
    header_text.insertString( header_cursor, data["qualification"], 0 )
    header_text.insertControlCharacter( header_cursor, PARAGRAPH_BREAK, False )
    header_text.insertString( header_cursor, data["specialisation"], 0 )
    return doc, text, cursor
