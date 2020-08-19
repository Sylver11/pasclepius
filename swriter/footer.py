from com.sun.star.style.ParagraphAdjust import CENTER, LEFT, RIGHT, BLOCK, STRETCH
from com.sun.star.text.ControlCharacter import PARAGRAPH_BREAK, APPEND_PARAGRAPH, LINE_BREAK


def populateBottomTable(doc, text, data):
    bottom_table = doc.createInstance( "com.sun.star.text.TextTable" )
    bottom_table.initialize(5,3)
    bottom_table.setName('footer_table')
    styles = doc.StyleFamilies
    page_styles = styles.getByName("PageStyles")
    oDefaultStyle = page_styles.getByName("Standard")
    oDefaultStyle.FooterIsOn = True
    oDefaultStyle.setPropertyValue("BottomMargin", 500)
    footer_text = oDefaultStyle.getPropertyValue("FooterText")
    footer_cursor = footer_text.createTextCursor()
    footer_text = footer_text.insertTextContent(footer_cursor, bottom_table, 1)
    first_bottom_table_text = bottom_table.getCellByName("A1")
    first_bottom_table_text.setString(" Accounts Details:" )
    first_bottom_table_text = bottom_table.getCellByName("A2")
    first_bottom_table_text.setString(" Account Holder:" )
    first_bottom_table_text = bottom_table.getCellByName("A3")
    first_bottom_table_text.setString(" Bank:" )
    first_bottom_table_text = bottom_table.getCellByName("A4")
    first_bottom_table_text.setString(" Account Number:" )
    first_bottom_table_text = bottom_table.getCellByName("A5")
    first_bottom_table_text.setString(" Branch Code:" )
    first_bottom_table_text = bottom_table.getCellByName("B2")
    first_bottom_table_text.setString(data["bank_holder"])
    first_bottom_table_text = bottom_table.getCellByName("B3")
    first_bottom_table_text.setString(data["bank"])
    first_bottom_table_text = bottom_table.getCellByName("B4")
    first_bottom_table_text.setString(data["bank_account"])
    first_bottom_table_text = bottom_table.getCellByName("B5")
    first_bottom_table_text.setString(data["bank_branch"])
    first_bottom_table_text = bottom_table.getCellByName("C1")
    first_bottom_table_text.setString("Postal:" )
    first_bottom_table_text = bottom_table.getCellByName("C2")
    first_bottom_table_text.setString(data["practice_name"])
    first_bottom_table_text = bottom_table.getCellByName("C3")
    first_bottom_table_text.setString(data["pob"])
    first_bottom_table_text = bottom_table.getCellByName("C4")
    first_bottom_table_text.setString(data["city"])
    first_bottom_table_text = bottom_table.getCellByName("C5")
    first_bottom_table_text.setString(data["country"])
    range = bottom_table.getCellRangeByName("A1:C5")
    range.setPropertyValue( "CharFontName", "Liberation Serif" )
    range.setPropertyValue( "CharHeight", 7.5 )
    range.setPropertyValue("ParaAdjust", LEFT)
    otabseps = bottom_table.TableColumnSeparators
    relativeTableWidth = bottom_table.getPropertyValue( "TableColumnRelativeSum" )
    otabseps[0].Position = relativeTableWidth * 0.2
    otabseps[1].Position = relativeTableWidth * 0.8
    bottom_table.TableColumnSeparators = otabseps
    bottom_table.setPropertyValue("TableColumnSeparators", otabseps)
    return doc, text

