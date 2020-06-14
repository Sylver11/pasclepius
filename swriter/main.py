import os
import uno
from footer import populateBottomTable
from header import populateTopText 
from identity import identityTable
from unohelper import systemPathToFileUrl
from com.sun.star.beans import PropertyValue
from com.sun.star.style.ParagraphAdjust import CENTER, LEFT, RIGHT, BLOCK, STRETCH
from com.sun.star.text.ControlCharacter import PARAGRAPH_BREAK, APPEND_PARAGRAPH, LINE_BREAK
from com.sun.star.text.TextContentAnchorType import AS_CHARACTER
from com.sun.star.table import BorderLine2
from com.sun.star.awt import Size
from com.sun.star.text import TableColumnSeparator
from com.sun.star.lang import Locale

cursor = None

def saveDocument(doc, url):
    url = systemPathToFileUrl( url + '.odt')
    args = (PropertyValue('FilterName',0, 'writer8', 0),)
    doc.storeToURL(url, args)
    doc.dispose()

def configureBorders(doc, text, items):
    no_line = BorderLine2()
    no_line.Color = 0
    no_line.InnerLineWidth = 0
    no_line.LineDistance = 0
    no_line.LineStyle = 0
    no_line.LineWidth = 0
    no_line.OuterLineWidth = 0
    text_tables = doc.getTextTables()
    get_top_table = text_tables.getByIndex(0)
    table_top_border = get_top_table.TableBorder
    table_top_border.LeftLine = no_line
    table_top_border.RightLine = no_line
    table_top_border.TopLine = no_line
    table_top_border.BottomLine = no_line
    table_top_border.HorizontalLine = no_line
    table_top_border.VerticalLine = no_line
    get_top_table.TableBorder = table_top_border
    get_middle_table =  text_tables.getByIndex(1)
    table_middle_border = get_middle_table.TableBorder
    table_middle_border.LeftLine = no_line
    table_middle_border.RightLine = no_line
    table_middle_border.TopLine = no_line
    table_middle_border.BottomLine = no_line
    table_middle_border.HorizontalLine = no_line
    table_middle_border.VerticalLine = no_line
    get_middle_table.TableBorder = table_middle_border
    get_main_table =  text_tables.getByIndex(2)
    count = 0
    col = ['A', 'B', 'C', 'D']
    for i in items:
        count = count + 1

    for i in col:
        table_main_cell = get_main_table.getCellByName(i + str(count+2))
        left_border_a_cell = table_main_cell.LeftBorder
        left_border_a_cell.OuterLineWidth = 0
        left_border_a_cell.LineWidth = 0
        table_main_cell.LeftBorder = left_border_a_cell

    cRange = get_main_table.getCellRangeByName("A" + str(count +2) + ":D" + str(count + 2))
    cRange.setPropertyValue( "CharFontName", "Liberation Serif" )
    cRange.setPropertyValue( "CharHeight", 10.0 )
    table_main_cell = get_main_table.getCellByName("D" + str(count+2))
    right_border_a_cell = table_main_cell.RightBorder
    right_border_a_cell.OuterLineWidth = 0
    right_border_a_cell.LineWidth = 0
    table_main_cell.RightBorder = right_border_a_cell
    table_main_border = get_main_table.TableBorder
    table_main_border.BottomLine = no_line
    get_main_table.TableBorder = table_main_border
    get_bottom_table =  text_tables.getByIndex(3)
    table_bottom_border = get_bottom_table.TableBorder
    table_bottom_border.Distance = 50
    table_bottom_border.HorizontalLine = no_line
    table_bottom_border.VerticalLine = no_line
    get_bottom_table.TableBorder = table_bottom_border
    return doc, text


def createTable(doc, text, unitCount):
    global cursor
    table = doc.createInstance( "com.sun.star.text.TextTable" )
    table.initialize(unitCount + 2, 4)
    text.insertTextContent( cursor, table, 1 )
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

def populateTable(doc, text, items, treatments, price, dates, modifier=None):
    table, unitCount = createTable(doc, text, len(treatments))
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




def setupConnection():
    localContext = uno.getComponentContext()
    resolver = localContext.ServiceManager.createInstanceWithContext("com.sun.star.bridge.UnoUrlResolver", localContext )
    smgr = resolver.resolve( "uno:socket,host=localhost,port=2002;urp;StarOffice.ServiceManager" )
    remoteContext = smgr.getPropertyValue( "DefaultContext" )
    desktop = smgr.createInstanceWithContext( "com.sun.star.frame.Desktop",remoteContext)
    doc = desktop.loadComponentFromURL( "private:factory/swriter","_blank", 0, () )
    text = doc.Text
    return doc, text

def createTextInvoice(items, treatments, price, dates, patient, modifier,
                      url, invoice_name, date_invoice, data):
    global cursor
    doc, text = setupConnection()
    cursor = text.createTextCursor()
    doc, text, cursor = populateTopText(cursor, doc, text, data)
    doc, text, cursor = identityTable(doc, text, cursor, patient, data)
    doc, text, cursor = populateMiddleTable(doc, text, cursor, patient, invoice_name,
                                    date_invoice)
    doc, text = populateTable(doc, text, items, treatments, price, dates, modifier)
    doc, text = populateBottomTable(doc, text, data)
    doc, text = configureBorders(doc, text, items)
    saveDocument(doc, url)


def testing():
    patient = {'case': 'asdfasdfa', 'csrf_token':'ImU5NjFiYWEwN2Y1MGUyMmFiZDBkY2ZiYTQ5NDgxYzdiN2NlODQ2MDQi.XpVy6A.zOXe-xkr0gUZJroWUQHqVEoGxu0','date': '2020-04-14', 'medical': 'mva', 'name': 'todayyy', 'po': '423423423'}
    dates = ['01-04-2020', '04-04-2020', '10-04-2020', '15-04-2020']
    treatments = [{'description': 'Infra-red, Radiant heat, Wax therapy Hot packs', 'units': 10, 'value': 98}, {'description': 'Infra-red, Radiant heat, Wax therapy Hot packs', 'units': 10, 'value': 98}, {'description': 'Infra-red, Radiant heat, Wax therapy Hot packs', 'units': 10, 'value': 98}, {'description': 'Infra-red, Radiant heat, Wax therapy Hot packs', 'units': 10, 'value': 98}]
    items = ['001', '001', '001', '001']
    price = ['300.45','435.25', '196', '444']
    modifier = ['0','0','0','14']
    url ='some/weird/url'
    invoice_name = 'soemwierdname'
    createTextInvoice(items, treatments, price, dates, patient, modifier, url,
                     invoice_name)

if __name__ == '__main__':
    import argparse
    import json
    parser = argparse.ArgumentParser(description='Creating an invoice')
    parser.add_argument('items',type=json.loads, help='this is a item list')
    parser.add_argument('treatments', type=json.loads, help='This should be a treatment list')
    parser.add_argument('price', type=json.loads, help='this should be a price list')
    parser.add_argument('dates', type=json.loads, help='this should be a dates list')
    parser.add_argument('patient', type=json.loads)
    parser.add_argument('modifier', type=json.loads, help='this should be a modifier list')
    parser.add_argument('url', type=json.loads, help='this should be a modifier list')
    parser.add_argument('invoice_name', type=json.loads, help='this should be a modifier list')
    parser.add_argument('date_invoice',type=json.loads)
    parser.add_argument('data', type=json.loads, help='the general data stuff')
    args = parser.parse_args()
    createTextInvoice(args.items, args.treatments, args.price, args.dates,
                      args.patient, args.modifier, args.url, args.invoice_name,
                      args.date_invoice, args.data)
   # testing()
