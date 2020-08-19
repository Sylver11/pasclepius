from com.sun.star.style.ParagraphAdjust import CENTER, LEFT, RIGHT, BLOCK, STRETCH
from com.sun.star.text.ControlCharacter import PARAGRAPH_BREAK, APPEND_PARAGRAPH, LINE_BREAK


def populateTopText(cursor, doc, text, practice):
    styles = doc.StyleFamilies
    page_styles = styles.getByName("PageStyles")
    oDefaultStyle = page_styles.getByName("Standard")
    oDefaultStyle.HeaderIsOn = True
    oDefaultStyle.setPropertyValue("TopMargin", 500)
    header_text = oDefaultStyle.getPropertyValue("HeaderText")
    header_cursor = header_text.createTextCursor()
    header_cursor.setPropertyValue( "CharFontName", "Liberation Serif" )
    header_cursor.setPropertyValue( "CharHeight", 18.0 )
    header_cursor.setPropertyValue( "ParaAdjust", CENTER )
    header_text.insertString(header_cursor, str(practice["practice_name"]), 0)
    header_text.insertControlCharacter( header_cursor, PARAGRAPH_BREAK, False )
    header_cursor.setPropertyValue( "CharHeight", 12.0 )
    header_text.insertString( header_cursor, practice["qualification"], 0 )
    header_text.insertControlCharacter( header_cursor, PARAGRAPH_BREAK, False )
    header_text.insertString( header_cursor, practice["specialisation"], 0 )
    header_text.insertControlCharacter( header_cursor, PARAGRAPH_BREAK, False )
    return doc, text, cursor
