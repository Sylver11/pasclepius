import os
import uno
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

def populateBottomTable(doc, text, data):
    bottom_table = doc.createInstance( "com.sun.star.text.TextTable" )
    bottom_table.initialize(5,3)
    bottom_table.setName('bottom_table')
    styles = doc.StyleFamilies
    page_styles = styles.getByName("PageStyles")
    oDefaultStyle = page_styles.getByName("Standard")
    oDefaultStyle.FooterIsOn = True
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
    first_bottom_table_text.setString(data["first_name"] +" " +  data["second_name"])
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

def populateMiddleTable(doc, text, patient, invoice_name, date_invoice):
    global cursor
    middle_table = doc.createInstance( "com.sun.star.text.TextTable" )
    if (patient['medical'] == 'mva'):
        middle_table.initialize(2,3)
        middle_table.setName('middle_table')
        text.insertTextContent( cursor, middle_table, 1 )
        first_middle_table_text = middle_table.getCellByName("A1")
        range_top = middle_table.getCellRangeByName("A1:A2")
        range_top.setPropertyValue( "ParaAdjust", LEFT )
        first_middle_table_text.setString("Invoice No: " + str(invoice_name))
        second_middle_table_text = middle_table.getCellByName("A2")
        second_middle_table_text.setString("Patient Name: " + str(patient['name']) + "\nCase Number: " + str(patient['case']) + "\nPO: " + str(patient['po']))
        cursor_middle_right = middle_table.createCursorByCellName("C1")
        cursor_middle_right.setPropertyValue( "ParaAdjust", RIGHT )
        cursor_middle_table_c1 = middle_table.getCellByName("C1")
        cursor_middle_table_c1.setString("Date: " + date_invoice[0])
        fourth_middle_table_text = middle_table.getCellByName("C2")
        fourth_middle_table_text.setString("Insurance: " + str(patient['medical']).upper())
        seventh_middle_table_text = middle_table.getCellByName("B1")
        seventh_middle_table_text.setString("Invoice")
        range = middle_table.getCellRangeByName("A1:C2")
        range.setPropertyValue( "CharFontName", "Liberation Serif" )
        range.setPropertyValue( "CharHeight", 10.0 )
        text.insertControlCharacter( cursor, PARAGRAPH_BREAK, False )

    else:
        middle_table.initialize(3,3)
        middle_table.setName('middle_table')
        text.insertTextContent( cursor, middle_table, 1 )
        first_middle_table_text = middle_table.getCellByName("A1")
        first_middle_table_text.setString("Invoice No: " + str(invoice_name))
        range_top = middle_table.getCellRangeByName("A1:A2")
        range_top.setPropertyValue( "ParaAdjust", LEFT )
        second_middle_table_text = middle_table.getCellByName("A2")
        second_middle_table_text.setString("Main Member: " + str(patient['main']))
        third_middle_table_text = middle_table.getCellByName("B2")
        third_middle_table_text.setString("Medical Aid No: " + str(patient['number']))
        cursor_middle_right = middle_table.createCursorByCellName("C1")
        cursor_middle_right.setPropertyValue( "ParaAdjust", RIGHT )
        cursor_middle_table_c1 = middle_table.getCellByName("C1")
        cursor_middle_table_c1.setString("Date: " + date_invoice[0])
        fourth_middle_table_text = middle_table.getCellByName("C2")
        fourth_middle_table_text.setString("Insurance: " + str(patient['medical']).upper())
        fifth_middle_table_text = middle_table.getCellByName("A3")
        fifth_middle_table_text.setString("Patient Name: " + str(patient['name']))
        sixth_middle_table_text = middle_table.getCellByName("B3")
        sixth_middle_table_text.setString("Patient DoB: " + str(patient['dob']))
        seventh_middle_table_text = middle_table.getCellByName("B1")
        seventh_middle_table_text.setString("Invoice")
        range_bottom = middle_table.getCellRangeByName("A1:C3")
        range_bottom.setPropertyValue( "CharFontName", "Liberation Serif" )
        range_bottom.setPropertyValue( "CharHeight", 10.0 )
        text.insertControlCharacter( cursor, PARAGRAPH_BREAK, False )
    return doc, text

def populateTopTable(doc, text, patient, data):
    global cursor
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
    return doc, text

def populateTopText(doc, text, data):
    global cursor
    cursor = text.createTextCursor()
    cursor.setPropertyValue( "CharFontName", "Liberation Serif" )
    cursor.setPropertyValue( "CharHeight", 10.0 )
    cursor.setPropertyValue( "ParaAdjust", CENTER )
    text.insertString( cursor, data["practice_name"], 0 )
    text.insertControlCharacter( cursor, PARAGRAPH_BREAK, False )
    text.insertString( cursor, data["qualification"], 0 )
    text.insertControlCharacter( cursor, PARAGRAPH_BREAK, False )
    text.insertControlCharacter( cursor, PARAGRAPH_BREAK, False )
    text.insertControlCharacter( cursor, PARAGRAPH_BREAK, False )
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
    doc, text = setupConnection()
    doc, text = populateTopText(doc, text, data)
    doc, text = populateTopTable(doc, text, patient, data)
    doc, text = populateMiddleTable(doc, text, patient, invoice_name,
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
