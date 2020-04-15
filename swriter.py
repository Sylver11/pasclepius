import uno
from unohelper import systemPathToFileUrl
from com.sun.star.beans import PropertyValue
from com.sun.star.style.ParagraphAdjust import CENTER, LEFT, RIGHT, BLOCK, STRETCH
from com.sun.star.text.ControlCharacter import PARAGRAPH_BREAK, APPEND_PARAGRAPH, LINE_BREAK
from com.sun.star.text.TextContentAnchorType import AS_CHARACTER
from com.sun.star.table import BorderLine2
from com.sun.star.awt import Size
from com.sun.star.text import TableColumnSeparator
cursor = None

def saveDocument(doc, patient):
    url = systemPathToFileUrl('/Users/justusvoigt/Documents/' + str(patient['case']) + '.odt')
    args = (PropertyValue('FilterName',0, 'writer8', 0),)
    doc.storeToURL(url, args)
    doc.dispose()

def configureBorders(doc, text):
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
    get_bottom_table =  text_tables.getByIndex(3)
    table_bottom_border = get_bottom_table.TableBorder
    table_bottom_border.HorizontalLine = no_line
    table_bottom_border.VerticalLine = no_line
    get_bottom_table.TableBorder = table_bottom_border
    return doc, text

def populateBottomTable(doc, text):
    global cursor
    bottom_table = doc.createInstance( "com.sun.star.text.TextTable" )
    bottom_table.initialize(5,3)
    bottom_table.setName('bottom_table')
    text.insertTextContent( cursor, bottom_table, 1 )
    first_bottom_table_text = bottom_table.getCellByName("A1")
    first_bottom_table_text.setString("Accounts Details:" )
    first_bottom_table_text = bottom_table.getCellByName("A2")
    first_bottom_table_text.setString("Account Holder:" )
    first_bottom_table_text = bottom_table.getCellByName("A3")
    first_bottom_table_text.setString("Bank:" )
    first_bottom_table_text = bottom_table.getCellByName("A4")
    first_bottom_table_text.setString("Account Number:" )
    first_bottom_table_text = bottom_table.getCellByName("A5")
    first_bottom_table_text.setString("Branch Code:" )
    first_bottom_table_text = bottom_table.getCellByName("B2")
    first_bottom_table_text.setString("A.Pickel-Voigt" )
    first_bottom_table_text = bottom_table.getCellByName("B3")
    first_bottom_table_text.setString("Standard Bank" )
    first_bottom_table_text = bottom_table.getCellByName("B4")
    first_bottom_table_text.setString("241710812" )
    first_bottom_table_text = bottom_table.getCellByName("B5")
    first_bottom_table_text.setString("084873 (Oshakati Branch)" )
    first_bottom_table_text = bottom_table.getCellByName("C1")
    first_bottom_table_text.setString("Postal:" )
    first_bottom_table_text = bottom_table.getCellByName("C2")
    first_bottom_table_text.setString("PO Box 37" )
    first_bottom_table_text = bottom_table.getCellByName("C3")
    first_bottom_table_text.setString("Oshakati" )
    first_bottom_table_text = bottom_table.getCellByName("C4")
    first_bottom_table_text.setString("Namibia" )
    return doc, text

def createTable(doc, text, unitCount):
    global cursor
    table = doc.createInstance( "com.sun.star.text.TextTable" )
    table.initialize(unitCount + 2, 4)
    text.insertTextContent( cursor, table, 1 )
    otabseps = table.TableColumnSeparators
    relativeTableWidth = table.getPropertyValue( "TableColumnRelativeSum" )
    otabseps[0].Position = relativeTableWidth * 0.10
    otabseps[1].Position = relativeTableWidth * 0.2
    otabseps[2].Position = relativeTableWidth * 0.85
    table.TableColumnSeparators = otabseps 
    table.setPropertyValue("TableColumnSeparators", otabseps)
    cRange = table.getCellRangeByName("A1:D1")
    cRange.setPropertyValue( "ParaAdjust", LEFT )
    insertTextIntoCell( table, "A1", "Date of Service" )
    insertTextIntoCell( table, "B1", "Namaf Code" )
    insertTextIntoCell( table, "C1", "Description")
    insertTextIntoCell( table, "D1", "Amount")
    insertTextIntoCell( table, "C" + str(2 + unitCount), "NS")
    cursor_right = table.createCursorByCellName("C" + str(2 + unitCount))
    cursor_right.setPropertyValue( "ParaAdjust", RIGHT )
    text.insertControlCharacter( cursor, PARAGRAPH_BREAK, False )
    return table, unitCount

def insertTextIntoCell( table, cellName, text, color = None ):
    tableText = table.getCellByName( cellName )
    cursor = tableText.createTextCursor()
    if color != None: 
        cursor.setPropertyValue( "CharColor", color )
    tableText.setString( text )

def populateTable(doc, text, items, treatments, dates):
    table, unitCount = createTable(doc, text, len(treatments))
    for a, b, c in zip(enumerate(treatments), dates, items):
        insertTextIntoCell(table, "B" + str(a[0] + 2), c)
        insertTextIntoCell(table, "A" + str(a[0] + 2), b)
        insertTextIntoCell(table, "C" + str(a[0] + 2), a[1]['description'])
        insertTextIntoCell(table, "D" + str(a[0] + 2), str(a[1]['value']))
    table.getCellByName("D" + str(2 + unitCount)).setFormula("=sum <D2:D" + str(1 + unitCount) + ">")
    return doc, text

def populateMiddleTable(doc, text, patient):
    global cursor
    middle_table = doc.createInstance( "com.sun.star.text.TextTable" )
    middle_table.initialize(2,3)
    middle_table.setName('middle_table')
    text.insertTextContent( cursor, middle_table, 1 )
    first_middle_table_text = middle_table.getCellByName("A1")
    first_middle_table_text.setString("Invoice No: MVA/2020/H" )
    second_middle_table_text = middle_table.getCellByName("A2")
    second_middle_table_text.setString("Patient Name: " + str(patient['name']))
    third_middle_table_text = middle_table.getCellByName("B2")
    third_middle_table_text.setString("Case Number: " + str(patient['case'])) 
    cursor_middle_right = middle_table.createCursorByCellName("C1")
    cursor_middle_right.setPropertyValue( "ParaAdjust", RIGHT )
    middle_table.getCellByName("C1").setString("Invoice Date: " + str(patient['date']))
    fourth_middle_table_text = middle_table.getCellByName("C2")
    fourth_middle_table_text.setString("PO: " + str(patient['po']))
    text.insertControlCharacter( cursor, PARAGRAPH_BREAK, False )
    return doc, text

def populateTopTable(doc, text, patient):
    print(patient['name'])
    global cursor
    cursor.setPropertyValue( "CharHeight", 10.0 )
    top_table = doc.createInstance( "com.sun.star.text.TextTable" )
    top_table.initialize(1,2)
    top_table.setName('top_Table')
    text.insertTextContent( cursor, top_table, 1 )
    first_top_table_text = top_table.getCellByName("A1")
    first_top_table_text.setString("Practice No: 072 0000 637653 \nHPCNA No: PHY 00194" )
    cursor_top_right = top_table.createCursorByCellName("B1")
    cursor_top_right.setPropertyValue( "ParaAdjust", RIGHT )
    top_table.getCellByName("B1").setString("anpickel@gmail.com \nCell: 081 648 11 82")
    eText = top_table.getCellByName("B1").getText()
    eCursor = eText.createTextCursor()
    eText.insertString(eCursor, "", False)
    eCursor.goRight(len("anpickel@gmail.com"), True)
    eCursor.HyperLinkURL = "mailto:anpickel@gmail.com"
    text.insertControlCharacter( cursor, PARAGRAPH_BREAK, False );
    return doc, text

def populateTopText(doc, text):
    global cursor
    cursor = text.createTextCursor()
    cursor.setPropertyValue( "CharFontName", "Liberation Serif" )
    cursor.setPropertyValue( "CharHeight", 10.0 )
    cursor.setPropertyValue( "ParaAdjust", CENTER )
    text.insertString( cursor, "A. Pickel-Voigt", 0 )
    text.insertControlCharacter( cursor, PARAGRAPH_BREAK, False )
    text.insertString( cursor, "MSc Physiotherapy (UWC)" , 0 )
    text.insertControlCharacter( cursor, PARAGRAPH_BREAK, False )
    text.insertControlCharacter( cursor, PARAGRAPH_BREAK, False );
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

def createTextInvoice(items, treatments, dates, patient):
    doc, text = setupConnection()
    doc, text = populateTopText(doc, text)
    doc, text = populateTopTable(doc, text, patient)
    doc, text = populateMiddleTable(doc, text, patient)
    doc, text = populateTable(doc, text, items, treatments, dates)
    doc, text = populateBottomTable(doc, text)
    doc, text = configureBorders(doc, text)
    saveDocument(doc, patient)


def testing():
    patient = {'case': 'asdfasdfa', 'csrf_token': 'ImU5NjFiYWEwN2Y1MGUyMmFiZDBkY2ZiYTQ5NDgxYzdiN2NlODQ2MDQi.XpVy6A.zOXe-xkr0gUZJroWUQHqVEoGxu0', 'date': '2020-04-14', 'medical': 'psemas', 'name': 'asdfasdf', 'po': '423423423'}
    dates = ['2020-04-15', '2020-04-15', '2020-04-15', '2020-04-15']
    treatments = [{'description': 'Infra-red, Radiant heat, Wax therapy Hot packs', 'units': 10, 'value': 98}, {'description': 'Infra-red, Radiant heat, Wax therapy Hot packs', 'units': 10, 'value': 98}, {'description': 'Infra-red, Radiant heat, Wax therapy Hot packs', 'units': 10, 'value': 98}, {'description': 'Infra-red, Radiant heat, Wax therapy Hot packs', 'units': 10, 'value': 98}]
    items = ['001', '001', '001', '001']
    createTextInvoice(items, treatments, dates, patient)



testing()
#populateTable(2,["11.04.20","13.04.20"],[343,211],["This is the test description","this is the second description"],[600,199])




#row.setPropertyValue( "BackTransparent", uno.Bool(0) )
#row.setPropertyValue( "BackColor", 6710932 )
#table.TableColumnSeparators = otabseps
#table.initialize( unitCount,4)
#column = table.Columns 
#rows = table.Rows

#colOne = table.getColumns.getByIndex(0)
#col = table.Columns(1)
#col.Width(200)
#column.getCellRangeByName("A1:A4")
#columnOne = column.getByIndex(0).Position
#colOne.Width(20)
#columnOne.setPropertyValue( "Width", 30 )
#cRange = table.getCellRangeByName("A1:D1")
#cRange.setPropertyValue( "ParaAdjust", LEFT )
#otabseps = table.TableColumnSeparators#(1500 * 10000 / 21000, True)
#cursorTop = cRange.createCursorByRange()
#tcs = TableColumnSeparator(1500 * 10000 / 21000, True)
#print(otabseps[0])
#absoluteTableWidth = table.getPropertyValue( "Width" )
#dRatio = relativeTableWidth / absoluteTableWidth

#print(otabseps)
#dRelativeWidth =  2000 * dRatio
#print(relativeTableWidth)
#print(relativeTableWidth * 0.05)
#print(otabseps[0].Position)
#otabseps[3].Position = relativeTableWidth * 0.3
#table.setPropertyValue( "BackTransparent", uno.Bool(0) )
#table.setPropertyValue( "BackColor", 13421823 )
#row = rows.getByIndex(0)
#table.getCellByName("D2").setFormula("sum <A2:C2>")

#table.getCellByName("A3").setValue(21.5)
#table.getCellByName("B3").setValue(615.3)
#table.getCellByName("C3").setValue(-315.7)
#table.getCellByName("D3").setFormula("sum <A3:C3>")

#table.getCellByName("A4").setValue(121.5)
#table.getCellByName("B4").setValue(-615.3)
#table.getCellByName("C4").setValue(415.7)
#table.getCellByName("D4").setFormula("sum <A4:C4>")


#cursor.setPropertyValue( "CharColor", 255 )
#cursor.setPropertyValue( "CharShadowed", uno.Bool(1) )

#text.insertControlCharacter( cursor, PARAGRAPH_BREAK, 0 )
#text.insertString( cursor, " This is a colored Text - blue with shadow\n" , 0 )
#text.insertControlCharacter( cursor, PARAGRAPH_BREAK, 0 )

#textFrame = doc.createInstance( "com.sun.star.text.TextFrame" )
#textFrame.setSize( Size(15000,400))
#textFrame.setPropertyValue( "AnchorType" , AS_CHARACTER )
#text.insertTextContent( cursor, textFrame, 0 )

#textInTextFrame = textFrame.getText()
#cursorInTextFrame = textInTextFrame.createTextCursor()
#textInTextFrame.insertString( cursorInTextFrame, "The first line in the newly created text frame.", 0 )
#textInTextFrame.insertString( cursorInTextFrame, "\nWith this second line the height of the rame raises.",0)
#textInTextFrame.insertControlCharacter( cursorInTextFrame, PARAGRAPH_BREAK, 0 )
#text.insertControlCharacter( cursor, PARAGRAPH_BREAK, 0 )

#cursor.setPropertyValue( "CharColor", 65536 )
#cursor.setPropertyValue( "CharShadowed", False )

#text.insertString( cursor, " That's all for now !!" , 0 )	
