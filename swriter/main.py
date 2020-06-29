import os
import uno
from footer import populateBottomTable
from header import populateTopText
from patient import patientTable
from treatment import treatmentTable
from identity import identityTable
from hospital import hospitalTable
from diagnosis import diagnosisTable
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


def createTextInvoice(layout, items, treatments, price, dates, patient, modifier,
                      url, invoice_name, date_invoice, data):
    doc, text = setupConnection()
    cursor = text.createTextCursor()
    doc, text, cursor = populateTopText(cursor, doc, text, data)
    doc, text, cursor = identityTable(doc, text, cursor, layout, patient, data)
    doc, text, cursor = patientTable(doc, text, cursor, patient, invoice_name,
                                    date_invoice)
    if 4 <= layout <= 9:
        doc, text, cursor = hospitalTable(doc, text, cursor, patient)
    if 7 <= layout <= 12:
        doc, text, cursor = diagnosisTable(doc, text, cursor, patient)
    doc, text = treatmentTable(doc, text, cursor, items, treatments, price, dates, modifier)
    doc, text = populateBottomTable(doc, text, data)
    doc, text = configureBorders(doc, text, items)
    saveDocument(doc, url)


if __name__ == '__main__':
    import argparse
    import json
    parser = argparse.ArgumentParser(description='Creating an invoice')
    parser.add_argument('to_json', type=json.loads)
    args = parser.parse_args()
    createTextInvoice(args.to_json['layout'],
            args.to_json['treatments'],
            args.to_json["treatment_list"],
            args.to_json["prices"],
            args.to_json["dates"],
            args.to_json["patient"],
            args.to_json["modifiers"],
            args.to_json["url"],
            args.to_json["invoice_name"],
            args.to_json["date_invoice"],
            args.to_json["data"])
