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
    return table, unitCount

def insertTextIntoCell( table, cellName, text, color = None ):
    tableText = table.getCellByName( cellName )
    cursor = tableText.createTextCursor()
    cursor.setPropertyValue( "CharFontName", "Liberation Serif" )
    cursor.setPropertyValue( "CharHeight", 9.0 )
    if color != None:
        cursor.setPropertyValue( "CharColor", color )
    tableText.setString( text )

def treatmentTable(doc, text, cursor, items, treatments, price, dates, patient, modifier=None):
    table, unitCount = createTable(doc, text, cursor, len(treatments))
    if not modifier:
        modifier=[]
        for x in range(len(treatments)):
            modifier.append('')
    for a, b, c, d, e in zip(enumerate(treatments), dates, items, price, modifier):
        if e == '14' or e == '13' or e == '10':
            insertTextIntoCell(table, "A" + str(a[0] + 2), str(c.zfill(3) + " (0" + e + ")"))
        elif e == '6' or e == '8' or e == '9':
            insertTextIntoCell(table, "A" + str(a[0] + 2), str(c.zfill(3) + " (00" + e + ")"))
        elif('namaf_orthopaedic_surgeons' in patient['tariff']):
            insertTextIntoCell(table, "A" + str(a[0] + 2), c.zfill(4))
        else:
            insertTextIntoCell(table, "A" + str(a[0] + 2), c.zfill(3))
        units_float = float(a[1]['units']) / 100
        insertTextIntoCell(table, "D" + str(a[0] + 2), b)
        insertTextIntoCell(table, "B" + str(a[0] + 2), a[1]['description'])
        insertTextIntoCell(table, "C" + str(a[0] + 2), units_float)
        insertTextIntoCell(table, "E" + str(a[0] + 2), d)
    cell_sum = table.getCellByName("E" + str(2 + unitCount))
    cell_sum.setFormula("=sum <E2:E" + str(1 + unitCount) + ">")
    cRange = table.getCellRangeByName("E2:E" + str(2 + unitCount) )
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

