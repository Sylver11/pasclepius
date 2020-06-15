from com.sun.star.style.ParagraphAdjust import CENTER, LEFT, RIGHT, BLOCK, STRETCH
from com.sun.star.text.ControlCharacter import PARAGRAPH_BREAK, APPEND_PARAGRAPH, LINE_BREAK
from com.sun.star.lang import Locale

def createTable(doc, text, cursor, unitCount):
    table = doc.createInstance( "com.sun.star.text.TextTable" )
    table.initialize(unitCount + 2, 4)
    text.insertTextContent( cursor, table, 1 )
    table.setName('treatment_table')
    otabseps = table.TableColumnSeparators
    relativeTableWidth = table.getPropertyValue( "TableColumnRelativeSum" )
    otabseps[0].Position = relativeTableWidth * 0.12
    otabseps[1].Position = relativeTableWidth * 0.21
    otabseps[2].Position = relativeTableWidth * 0.90
    table.TableColumnSeparators = otabseps
    table.setPropertyValue("TableColumnSeparators", otabseps)
    cRange = table.getCellRangeByName("A1:D1")
    cRange.setPropertyValue( "CharFontName", "Liberation Serif" )
    cRange.setPropertyValue( "CharHeight", 10.0 )
    insertTextIntoCell( table, "A1", "Date of Service" )
    insertTextIntoCell( table, "B1", "Namaf Code" )
    insertTextIntoCell( table, "C1", "Description")
    insertTextIntoCell( table, "D1", "Amount")
    insertTextIntoCell( table, "C" + str(2 + unitCount), "Total N$: ")
    cursor_right = table.createCursorByCellName("C" + str(2 + unitCount))
    cursor_right.setPropertyValue( "ParaAdjust", RIGHT )
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

def treatmentTable(doc, text, cursor, items, treatments, price, dates, modifier=None):
    table, unitCount = createTable(doc, text, cursor, len(treatments))
    if not modifier:
        modifier=[]
        for x in range(len(treatments)):
            modifier.append('')
    for a, b, c, d, e in zip(enumerate(treatments), dates, items, price, modifier):
        if e == '14' or e == '13' or e == '10':
            insertTextIntoCell(table, "B" + str(a[0] + 2), str(c + " (0" + e + ")"))
        elif e == '6' or e == '8' or e == '9':
            insertTextIntoCell(table, "B" + str(a[0] + 2), str(c + " (00" + e + ")"))
        else:
            insertTextIntoCell(table, "B" + str(a[0] + 2), c)
        insertTextIntoCell(table, "A" + str(a[0] + 2), b)
        insertTextIntoCell(table, "C" + str(a[0] + 2), a[1]['description'])
        insertTextIntoCell(table, "D" + str(a[0] + 2), d)
    cell_sum = table.getCellByName("D" + str(2 + unitCount))
    cell_sum.setFormula("=sum <D2:D" + str(1 + unitCount) + ">")
    cRange = table.getCellRangeByName("D2:D" + str(2 + unitCount) )
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

