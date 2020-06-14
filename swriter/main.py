import os
import uno
from footer import populateBottomTable
from header import populateTopText
from patient import patientTable
from treatment import treatmentTable
from identity import identityTable
from border import configureBorders
from unohelper import systemPathToFileUrl
from com.sun.star.beans import PropertyValue


def saveDocument(doc, url):
    url = systemPathToFileUrl( url + '.odt')
    args = (PropertyValue('FilterName',0, 'writer8', 0),)
    doc.storeToURL(url, args)
    doc.dispose()


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
    cursor = text.createTextCursor()
    doc, text, cursor = populateTopText(cursor, doc, text, data)
    doc, text, cursor = identityTable(doc, text, cursor, patient, data)
    doc, text, cursor = patientTable(doc, text, cursor, patient, invoice_name,
                                    date_invoice)
    doc, text = treatmentTable(doc, text, cursor, items, treatments, price, dates, modifier)
    doc, text = populateBottomTable(doc, text, data)
    doc, text = configureBorders(doc, text, items)
    saveDocument(doc, url)


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
