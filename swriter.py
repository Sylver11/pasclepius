# bootstrap uno component context 	
import uno
import unohelper


# a UNO struct later needed to create a document
from com.sun.star.style.ParagraphAdjust import CENTER, LEFT, RIGHT, BLOCK, STRETCH
from com.sun.star.text.ControlCharacter import PARAGRAPH_BREAK, APPEND_PARAGRAPH, LINE_BREAK
from com.sun.star.text.TextContentAnchorType import AS_CHARACTER
from com.sun.star.awt import Size
#from com.sun.star.table import BorderLine
#from com.sun.star.rendering.Text
from com.sun.star.text import TableColumnSeparator
#aSize = uno.createUnoStruct('com.sun.star.awt.Size')
localContext = uno.getComponentContext()
				   
resolver = localContext.ServiceManager.createInstanceWithContext(
				"com.sun.star.bridge.UnoUrlResolver", localContext )

smgr = resolver.resolve( "uno:socket,host=localhost,port=2002;urp;StarOffice.ServiceManager" )
remoteContext = smgr.getPropertyValue( "DefaultContext" )

#remoteContext = resolver.resolve( "uno:socket,host=localhost,port=2002;urp;StarOffice.ComponentContext" )
#smgr = remoteContext.ServiceManager

desktop = smgr.createInstanceWithContext( "com.sun.star.frame.Desktop",remoteContext)

# open a writer document
doc = desktop.loadComponentFromURL( "private:factory/swriter","_blank", 0, () )
text = doc.Text
cursor = text.createTextCursor()
cursor.setPropertyValue( "CharFontName", "Liberation Serif" )
cursor.setPropertyValue( "CharHeight", 10.0 )
cursor.setPropertyValue( "ParaAdjust", CENTER )
text.insertString( cursor, "A. Pickel-Voigt", 0 )
text.insertControlCharacter( cursor, PARAGRAPH_BREAK, False );
text.insertString( cursor, "MSc Physiotherapy (UWC)" , 0 )
text.insertControlCharacter( cursor, PARAGRAPH_BREAK, False );



topTable = doc.createInstance( "com.sun.star.text.TextTable" )
topTable.initialize( 1,2)
text.insertTextContent( cursor, topTable, 1 )
firsttopTableText = topTable.getCellByName("A1")
firsttopTableText.setString("Practice No: 072 0000 637653" )

#aSize = uno.createUnoStruct('com.sun.star.table.BorderLine')
#bSize = uno.createUnoStruct('com.sun.star.table.TableBorder')
#aSize.TableLine = "TopLine"
#aSize.TopLine
#aSize.OuterLineWidth
#bSize.TopLine   
#aSize.Color = 255 

cursorTopRight = topTable.createCursorByCellName("B1")
cursorTopRight.setPropertyValue( "ParaAdjust", RIGHT )
topTable.getCellByName("B1").setString("anpickel@gmail.com")
eText = topTable.getCellByName("B1").getText()
eCursor = eText.createTextCursor()
eText.insertString(eCursor, "", False)
eCursor.goRight(len("anpickel@gmail.com"), True)
eCursor.HyperLinkURL = "mailto:anpickel@gmail.com"



text.insertControlCharacter( cursor, PARAGRAPH_BREAK, False );


def insertTextIntoCell( table, cellName, text, color = None ):
    tableText = table.getCellByName( cellName )
    cursor = tableText.createTextCursor()
    if color != None: 
        cursor.setPropertyValue( "CharColor", color )
    tableText.setString( text )



def createTable(unitCount):
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
    table.getCellByName("D" + str(2 + unitCount)).setFormula("sum <D2:D" + str(1 + unitCount) + ">")
    return table



def populateTable(unitCount, unitDate,  unitCode, unitDescription, unitAmount):
    table = createTable(unitCount)
    for i in range(len(unitDate)):
        insertTextIntoCell(table, "A" +  str(i + 2), unitDate[i])
    for i in range(len(unitCode)):
        table.getCellByName("B" + str(i + 2)).setValue(unitCode[i])
    for i in range(len(unitDescription)):
        insertTextIntoCell(table, "C" + str(i + 2), unitDescription[i])
    for i in range(len(unitAmount)):
        insertTextIntoCell(table,"D" + str(i + 2), unitAmount[i])
    return None 


populateTable(2,["11.04.20","13.04.20"],[343,211],["This is the test description","this is the second description"],[600,199])




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

text.insertControlCharacter( cursor, PARAGRAPH_BREAK, 0 )
text.insertString( cursor, " This is a colored Text - blue with shadow\n" , 0 )
text.insertControlCharacter( cursor, PARAGRAPH_BREAK, 0 )

textFrame = doc.createInstance( "com.sun.star.text.TextFrame" )
textFrame.setSize( Size(15000,400))
textFrame.setPropertyValue( "AnchorType" , AS_CHARACTER )
text.insertTextContent( cursor, textFrame, 0 )

textInTextFrame = textFrame.getText()
cursorInTextFrame = textInTextFrame.createTextCursor()
textInTextFrame.insertString( cursorInTextFrame, "The first line in the newly created text frame.", 0 )
textInTextFrame.insertString( cursorInTextFrame, "\nWith this second line the height of the rame raises.",0)
textInTextFrame.insertControlCharacter( cursorInTextFrame, PARAGRAPH_BREAK, 0 )
text.insertControlCharacter( cursor, PARAGRAPH_BREAK, 0 )

cursor.setPropertyValue( "CharColor", 65536 )
cursor.setPropertyValue( "CharShadowed", False )

text.insertString( cursor, " That's all for now !!" , 0 )	
