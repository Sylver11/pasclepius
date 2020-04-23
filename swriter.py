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
    url = systemPathToFileUrl('/Users/justusvoigt/Documents/' + str(patient['name']) + '.odt')
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

    # in order to get the count can't you rather just do:
    # len(items)
    for i in items:
        count = count + 1

    for i in col:
        table_main_cell = get_main_table.getCellByName(i + str(count + 2))
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
    table_bottom_border.Distance = 1
    table_bottom_border.HorizontalLine = no_line
    table_bottom_border.VerticalLine = no_line
    get_bottom_table.TableBorder = table_bottom_border
    return doc, text

def populateBottomTable(doc, text):
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
    first_bottom_table_text.setString("A. Pickel-Voigt" )
    first_bottom_table_text = bottom_table.getCellByName("C3")
    first_bottom_table_text.setString("PO Box 37" )
    first_bottom_table_text = bottom_table.getCellByName("C4")
    first_bottom_table_text.setString("Oshakati" )
    first_bottom_table_text = bottom_table.getCellByName("C5")
    first_bottom_table_text.setString("Namibia" )
    range = bottom_table.getCellRangeByName("A1:C5")
    range.setPropertyValue( "CharFontName", "Liberation Serif" )
    range.setPropertyValue( "CharHeight", 8.5 )
    range.setPropertyValue("ParaAdjust", LEFT)
    otabseps = bottom_table.TableColumnSeparators
    relativeTableWidth = bottom_table.getPropertyValue( "TableColumnRelativeSum" )
    otabseps[0].Position = relativeTableWidth * 0.2
    otabseps[1].Position = relativeTableWidth * 0.8
   # otabseps[2].Position = relativeTableWidth * 0.90
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
    cRange.setPropertyValue( "ParaAdjust", LEFT )
    cRange.setPropertyValue( "CharFontName", "Liberation Serif" )
    cRange.setPropertyValue( "CharHeight", 10.0 )
    insertTextIntoCell( table, "A1", "Date of Service" )
    insertTextIntoCell( table, "B1", "Namaf Code" )
    insertTextIntoCell( table, "C1", "Description")
    insertTextIntoCell( table, "D1", "Amount")
    insertTextIntoCell( table, "C" + str(2 + unitCount), "Total N$: ")
   # insertTextIntoCell( table, "A" + str(2 + unitCount), "Total")
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

def populateTable(doc, text, items, treatments, price, dates, modifier):
    table, unitCount = createTable(doc, text, len(treatments))
    print(price)
    print(treatments)
    for a, b, c, d, e in zip(enumerate(treatments), dates, items, price, modifier):
        if e == '14':
            insertTextIntoCell(table, "B" + str(a[0] + 2), str(c + " (0" + e + ")"))
        else:
            insertTextIntoCell(table, "B" + str(a[0] + 2), c)
        insertTextIntoCell(table, "A" + str(a[0] + 2), b)
        insertTextIntoCell(table, "C" + str(a[0] + 2), a[1]['description'])
        insertTextIntoCell(table, "D" + str(a[0] + 2), str(d))
    cell_sum = table.getCellByName("D" + str(2 + unitCount))
    cell_sum.setFormula("=sum <D2:D" + str(1 + unitCount) + ">")
   # NumForms = doc.getNumberFormats()
   # dateFormatString = "YYYY/MM/DD\\ HH:MM:SS"
   # DateKey = NumForms.queryKey(dateFormatString, sLocale, True)
   # cell_sum.NumberFormat = DateKey
    return doc, text

def populateMiddleTable(doc, text, patient):
    global cursor
    middle_table = doc.createInstance( "com.sun.star.text.TextTable" )
    if (patient['medical'] == 'mva'):
        middle_table.initialize(2,3)
        middle_table.setName('middle_table')
        text.insertTextContent( cursor, middle_table, 1 )
        first_middle_table_text = middle_table.getCellByName("A1")
        first_middle_table_text.setString("Invoice No: MVA/2020/H" )
        first_middle_table_text.setPropertyValue( "ParaAdjust", LEFT )
        first_middle_table_text.setPropertyValue( "CharHeight", 10.0 )
        second_middle_table_text = middle_table.getCellByName("A2")
        second_middle_table_text.setString("Patient Name: " + str(patient['name']) + "\nCase Number: " + str(patient['case']) + "\nPO: " + str(patient['po']))
        second_middle_table_text.setPropertyValue( "CharFontName", "Liberation Serif" )
        second_middle_table_text.setPropertyValue( "CharHeight", 10.0 )
        third_middle_table_text = middle_table.getCellByName("B2")
       # third_middle_table_text.setString("Case Number: " + str(patient['case']))
        third_middle_table_text.setPropertyValue( "CharFontName", "Liberation Serif" )
        third_middle_table_text.setPropertyValue( "CharHeight", 10.0 )
       # third_middle_table_text.setPropertyValue("ParaAdjust", CENTER)
        cursor_middle_right = middle_table.createCursorByCellName("C1")
        cursor_middle_right.setPropertyValue( "ParaAdjust", RIGHT )
        cursor_middle_table_c1 = middle_table.getCellByName("C1")
        cursor_middle_table_c1.setString("Date: " + str(patient['date']))
        cursor_middle_table_c1.setPropertyValue( "CharFontName", "Liberation Serif" )
        cursor_middle_table_c1.setPropertyValue( "CharHeight", 10.0 )
        fourth_middle_table_text = middle_table.getCellByName("C2")
      #  fourth_middle_table_text.setString("PO: " + str(patient['po']))
        fourth_middle_table_text.setPropertyValue( "CharFontName", "Liberation Serif" )
        fourth_middle_table_text.setPropertyValue( "CharHeight", 10.0 )
       # fourth_middle_table_text.setPropertyValue( "ParaAdjust", RIGHT )
        
        seventh_middle_table_text = middle_table.getCellByName("B1")
        seventh_middle_table_text.setString("Invoice")
        seventh_middle_table_text.setPropertyValue( "CharFontName", "Liberation Serif" )
        seventh_middle_table_text.setPropertyValue( "CharHeight", 11.0 )



        text.insertControlCharacter( cursor, PARAGRAPH_BREAK, False )
       # text.insertControlCharacter( cursor, PARAGRAPH_BREAK, False )

    else:
        middle_table.initialize(3,3)
        middle_table.setName('middle_table')
        text.insertTextContent( cursor, middle_table, 1 )
        first_middle_table_text = middle_table.getCellByName("A1")
        first_middle_table_text.setString("Invoice No: PSEMAS/2020/H" )
        first_middle_table_text.setPropertyValue( "ParaAdjust", LEFT )
        first_middle_table_text.setPropertyValue( "CharHeight", 10.0 )
        second_middle_table_text = middle_table.getCellByName("A2")
        second_middle_table_text.setString("Main Member: " + str(patient['main']))
        second_middle_table_text.setPropertyValue( "CharFontName", "Liberation Serif" )
        second_middle_table_text.setPropertyValue( "CharHeight", 10.0 )
        third_middle_table_text = middle_table.getCellByName("B2")
        third_middle_table_text.setString("Medical Aid No: " + str(patient['number']))
        third_middle_table_text.setPropertyValue( "CharFontName", "Liberation Serif" )
        third_middle_table_text.setPropertyValue( "CharHeight", 10.0 )
       # third_middle_table_text.setPropertyValue("ParaAdjust", CENTER)
        cursor_middle_right = middle_table.createCursorByCellName("C1")
        cursor_middle_right.setPropertyValue( "ParaAdjust", RIGHT )
        cursor_middle_table_c1 = middle_table.getCellByName("C1")
        cursor_middle_table_c1.setString("Date: " + str(patient['date']))
        cursor_middle_table_c1.setPropertyValue( "CharFontName", "Liberation Serif" )
        cursor_middle_table_c1.setPropertyValue( "CharHeight", 10.0 )
        fourth_middle_table_text = middle_table.getCellByName("C2")
        fourth_middle_table_text.setString("Insurance: " + str(patient['medical']))
        fourth_middle_table_text.setPropertyValue( "CharFontName", "Liberation Serif" )
        fourth_middle_table_text.setPropertyValue( "CharHeight", 10.0 )
        #fourth_middle_table_text.setPropertyValue( "ParaAdjust", RIGHT )
        fifth_middle_table_text = middle_table.getCellByName("A3")
        fifth_middle_table_text.setString("Patient Name: " + str(patient['name']))
        fifth_middle_table_text.setPropertyValue( "CharFontName", "Liberation Serif" )
        fifth_middle_table_text.setPropertyValue( "CharHeight", 10.0 )
       # fifth_middle_table_text.setPropertyValue("ParaAdjust", CENTER)
        sixth_middle_table_text = middle_table.getCellByName("B3")
        sixth_middle_table_text.setString("Patient DoB: " + str(patient['dob']))
        sixth_middle_table_text.setPropertyValue( "CharFontName", "Liberation Serif" )
        sixth_middle_table_text.setPropertyValue( "CharHeight", 10.0 )
        
        seventh_middle_table_text = middle_table.getCellByName("B1")
        seventh_middle_table_text.setString("Invoice")
        seventh_middle_table_text.setPropertyValue( "CharFontName", "Liberation Serif" )
        seventh_middle_table_text.setPropertyValue( "CharHeight", 11.0 )


        #sixth_middle_table_text.setPropertyValue("ParaAdjust", CENTER)
        text.insertControlCharacter( cursor, PARAGRAPH_BREAK, False )
       # text.insertControlCharacter( cursor, PARAGRAPH_BREAK, False )

    return doc, text

def populateTopTable(doc, text, patient):
    global cursor
    cursor.setPropertyValue( "CharHeight", 10.0 )
    cursor.setPropertyValue( "CharFontName", "Liberation Serif" )
    top_table = doc.createInstance( "com.sun.star.text.TextTable" )
    top_table.initialize(1,2)
    top_table.setName('top_Table')
    text.insertTextContent( cursor, top_table, 1 )
    first_top_table_text = top_table.getCellByName("A1")
    first_top_table_text.setString("Practice No: 072 0000 637653 \nHPCNA No: PHY 00194" )
    first_top_table_text.setPropertyValue( "CharHeight", 10.0 )
    cursor_top_right = top_table.createCursorByCellName("B1")
    cursor_top_right.setPropertyValue( "ParaAdjust", RIGHT )
    second_top_table_text = top_table.getCellByName("B1")
    second_top_table_text.setPropertyValue( "CharHeight", 10.0 )
    second_top_table_text.setString("anpickel@gmail.com\nCell: 081 648 11 82")
    eText = top_table.getCellByName("B1").getText()
    eCursor = eText.createTextCursor()
    eText.insertString(eCursor, "", False)
    eCursor.goRight(len("anpickel@gmail.com"), True)
    eCursor.HyperLinkURL = "mailto:anpickel@gmail.com"
    text.insertControlCharacter( cursor, PARAGRAPH_BREAK, False );
    return doc, text

def populateTopText(doc, text):
    global cursor
#    styles = doc.StyleFamilies
#    page_styles = styles.getByName("PageStyles")
#    oDefaultStyle = page_styles.getByName("Standard")
#    oDefaultStyle.HeaderIsOn = True
#    header_text = oDefaultStyle.getPropertyValue("HeaderText")
#    header_cursor = header_text.createTextCursor()
#    header_text.insertString(header_cursor, "hello",0)

    cursor = text.createTextCursor()
    cursor.setPropertyValue( "CharFontName", "Liberation Serif" )
    cursor.setPropertyValue( "CharHeight", 10.0 )
    cursor.setPropertyValue( "ParaAdjust", CENTER )
    text.insertString( cursor, "A. Pickel-Voigt", 0 )
    text.insertControlCharacter( cursor, PARAGRAPH_BREAK, False )
    text.insertString( cursor, "MSc Physiotherapy (UWC)" , 0 )
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

def createTextInvoice(items, treatments, price, dates, patient, modifier):
    doc, text = setupConnection()
    doc, text = populateTopText(doc, text)
    doc, text = populateTopTable(doc, text, patient)
    doc, text = populateMiddleTable(doc, text, patient)
    doc, text = populateTable(doc, text, items, treatments, price, dates, modifier)
    doc, text = populateBottomTable(doc, text)
    doc, text = configureBorders(doc, text, items)
    saveDocument(doc, patient)


def testing():
    patient = {'case': 'asdfasdfa', 'csrf_token':'ImU5NjFiYWEwN2Y1MGUyMmFiZDBkY2ZiYTQ5NDgxYzdiN2NlODQ2MDQi.XpVy6A.zOXe-xkr0gUZJroWUQHqVEoGxu0','date': '2020-04-14', 'medical': 'mva', 'name': 'asdfasdf', 'po': '423423423'}
    dates = ['01-04-2020', '04-04-2020', '10-04-2020', '15-04-2020']
    treatments = [{'description': 'Infra-red, Radiant heat, Wax therapy Hot packs', 'units': 10, 'value': 98}, {'description': 'Infra-red, Radiant heat, Wax therapy Hot packs', 'units': 10, 'value': 98}, {'description': 'Infra-red, Radiant heat, Wax therapy Hot packs', 'units': 10, 'value': 98}, {'description': 'Infra-red, Radiant heat, Wax therapy Hot packs', 'units': 10, 'value': 98}]
    items = ['001', '001', '001', '001']
    price = ['300','435', '196', '444']
    modifier = ['0','0','0','14']
    createTextInvoice(items, treatments, price, dates, patient, modifier)

testing()
