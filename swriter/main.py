import os
import uno
from footer import populateBottomTable
from header import populateTopText
from patient import patientTable
from treatment_tables import namaf_orthopaedic_surgeons, namaf_physio
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


def createTextInvoice(user, invoice, treatments, descriptions, units,
        post_values, dates, modifiers):
    doc, text = setupConnection()
    cursor = text.createTextCursor()
    doc, text, cursor = populateTopText(cursor, doc, text, user)
    doc, text, cursor = identityTable(doc, text, cursor,  user, invoice)
    doc, text, cursor = patientTable(doc, text, cursor, invoice)
    if 4 <= int(invoice['invoice_layout']) <= 9:
        doc, text, cursor = hospitalTable(doc, text, cursor, invoice)
    if 7 <= int(invoice['invoice_layout']) <= 12:
        doc, text, cursor = diagnosisTable(doc, text, cursor, invoice)
    if 'orthopaedic_surgeons' in invoice['tariff']:
        doc, text = namaf_orthopaedic_surgeons.treatmentTable(doc,
                text, cursor, treatments, descriptions,
                units, post_values, dates)
    elif 'physio' in invoice['tariff']:
        doc, text = namaf_physio.treatmentTable(doc,
                text, cursor, treatments, descriptions,
                units, post_values, dates, modifiers)
    doc, text = populateBottomTable(doc, text, user)
    doc, text = configureBorders(doc, text, treatments)
    saveDocument(doc, invoice['invoice_file_url'])


if __name__ == '__main__':
    import argparse
    import json
    parser = argparse.ArgumentParser(description='Creating an invoice')
    parser.add_argument('to_json', type=json.loads)
    args = parser.parse_args()
    createTextInvoice(
            args.to_json["user"],
            args.to_json["invoice"],
            args.to_json["treatments"],
            args.to_json["descriptions"],
            args.to_json["units"],
            args.to_json["post_values"],
            args.to_json["dates"],
            args.to_json["modifiers"]
            )
