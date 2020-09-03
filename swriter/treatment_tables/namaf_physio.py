from com.sun.star.style.ParagraphAdjust import CENTER, LEFT, RIGHT, BLOCK, STRETCH
from com.sun.star.text.ControlCharacter import PARAGRAPH_BREAK, APPEND_PARAGRAPH, LINE_BREAK
from com.sun.star.lang import Locale
from com.sun.star.awt.FontWeight import BOLD as FW_BOLD


def createTable(doc, text, cursor, unitCount):
    table = doc.createInstance( "com.sun.star.text.TextTable" )
    table.initialize(unitCount + 2, 5)
    text.insertTextContent( cursor, table, 1 )
    table.setName('treatment_table')
    otabseps = table.TableColumnSeparators
    relativeTableWidth = table.getPropertyValue( "TableColumnRelativeSum" )
    otabseps[0].Position = 1080
    otabseps[1].Position = 6675
    otabseps[2].Position = 7755
    otabseps[3].Position = 8835
    table.TableColumnSeparators = otabseps
    table.setPropertyValue("TableColumnSeparators", otabseps)
    cRange = table.getCellRangeByName("A1:E1")
    cRange.setPropertyValue( "CharFontName", "Liberation Serif" )
    cRange.setPropertyValue( "CharHeight", 10.0 )
    insertTextIntoCell( table, "A1", "NAMAF Code" )
    insertTextIntoCell( table, "B1", "Description" )
    insertTextIntoCell( table, "C1", "Units")
    insertTextIntoCell( table, "D1", "Date")
    insertTextIntoCell( table, "E1", "Value")
    insertTextIntoCell( table, "D" + str(2 + unitCount), "Total N$: ")
    cursor_right = table.createCursorByCellName("D" + str(2 + unitCount))
    cursor_right.setPropertyValue( "ParaAdjust", RIGHT )
    bottom_range = table.getCellRangeByName("A" + str(2 + unitCount)
        + ":E" + str(2+ unitCount))
    bottom_range.setPropertyValue("CharWeight", FW_BOLD)
    text.insertControlCharacter( cursor, PARAGRAPH_BREAK, False )
    return table

def insertTextIntoCell( table, cellName, text, color = None ):
    tableText = table.getCellByName( cellName )
    cursor = tableText.createTextCursor()
    cursor.setPropertyValue( "CharFontName", "Liberation Serif" )
    cursor.setPropertyValue( "CharHeight", 9.0 )
    if color != None:
        cursor.setPropertyValue( "CharColor", color )
    tableText.setString( text )

def treatmentTable(doc, text, cursor, treatments, descriptions, units, post_values, dates,
        modifiers):
    table = createTable(doc, text, cursor, len(treatments))
    counter =  2
    for treatment, description, unit, post_value, date, modifier in zip(treatments, descriptions, units, post_values, dates, modifiers):
        if modifier == '14' or modifier == '13' or modifier == '10':
            insertTextIntoCell(table,
                    "A" + str(counter),
                    str(treatment.zfill(3) + " (0" + modifier + ")"))
        elif modifier == '6' or modifier == '8' or modifier == '9':
            insertTextIntoCell(table,
                    "A" + str(counter),
                    str(treatment.zfill(3) + " (00" + modifier + ")"))
        else:
            insertTextIntoCell(table, "A" + str(counter), treatment.zfill(3))
        insertTextIntoCell(table, "B" + str(counter), description)
        insertTextIntoCell(table, "C" + str(counter), unit)
        insertTextIntoCell(table, "D" + str(counter), date)
        insertTextIntoCell(table, "E" + str(counter), post_value)
        counter += 1
    cell_sum = table.getCellByName("E" + str(counter))
    cell_sum.setFormula("=sum <E2:E" + str(counter - 1) + ">")
    cRange = table.getCellRangeByName("E2:E" + str(counter) )
    xNumberFormats = doc.NumberFormats
    xLocale = Locale('en', 'US', '')
    format_string = '#,##0.00#'#[$€-407];[RED]-#,##0.00 [$€-407]'
    key = xNumberFormats.queryKey(format_string, xLocale, True)
    key = xNumberFormats.addNew(format_string, xLocale)
    cRange.NumberFormat = key
    cRange.setPropertyValue( "ParaAdjust", RIGHT )
   # NumForms = doc.getNumberFormats()
   # dateFormatString = "YYYY/MM/DD\\ HH:MM:SS"
   # DateKey = NumForms.queryKey(dateFormatString, sLocale, True)
   # cell_sum.NumberFormat = DateKey
    return doc, text

