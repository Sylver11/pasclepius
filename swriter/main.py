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


def createTextInvoice(user, patient, item_numbers, item_descriptions, item_values, item_dates, item_modifiers, invoice_file_url, invoice_id, date_invoice):
    doc, text = setupConnection()
    cursor = text.createTextCursor()
    doc, text, cursor = populateTopText(cursor, doc, text, user)
    doc, text, cursor = identityTable(doc, text, cursor,  user, patient)
    doc, text, cursor = patientTable(doc, text, cursor, patient, invoice_id,
                                    date_invoice)
    if 4 <= user['invoice_layout'] <= 9:
        doc, text, cursor = hospitalTable(doc, text, cursor, patient)
    if 7 <= user['invoice_layout'] <= 12:
        doc, text, cursor = diagnosisTable(doc, text, cursor, patient)
    doc, text = treatmentTable(doc, text, cursor, item_numbers,
            item_descriptions, item_values,
            item_dates, patient, item_modifiers)
    doc, text = populateBottomTable(doc, text, user)
    doc, text = configureBorders(doc, text, item_numbers)
    saveDocument(doc, invoice_file_url)


if __name__ == '__main__':
    import argparse
    import json
    parser = argparse.ArgumentParser(description='Creating an invoice')
    parser.add_argument('to_json', type=json.loads)
    args = parser.parse_args()
    createTextInvoice(
            args.to_json["user"],
            args.to_json["patient"],
            args.to_json["item_numbers"],
            args.to_json["item_descriptions"],
            args.to_json["item_values"],
            args.to_json["item_dates"],
            args.to_json["item_modifiers"],
            args.to_json["invoice_file_url"],
            args.to_json["invoice_id"],
            args.to_json["date_invoice"],
            )
