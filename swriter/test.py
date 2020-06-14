from main import createTextInvoice

def testing():
    data =  {'treatments': ['503', '901', '107'], 'treatment_list': [{'description': 'Rehabilitation for Central Nervous System disorders - condition to be clearly stated and fully documented (No other treatment modality may be charged in conjunction with this)', 'units': 55.0, 'value': 540.9}, {'description': 'Treatment at a nursing home: Relevant fee plus (to be charged only once per day and not with every hospital visit', 'units': 10.04, 'value': 98.7}, {'description': 'Interferential Therapy15', 'units': 15.0, 'value': 147.5}], 'prices': ['540.90', '98.70', '147.50'], 'dates': ['24.06.2020', '19.06.2020', '17.06.2020'], 'patient': {'csrf_token': 'IjU0Mjk1NDA4M2NhN2U5ODljNmQ4MGI5NzBmYTYwNDhjYzBmM2IzNzMi.XuaAiw.zgZzXdzZranOAmHGoBd_9uXTt-c', 'date': '16.06.2020', 'dob': '04.04.1992', 'main': 'Andreas Voigt', 'medical': 'Momentum ', 'name': 'Justus Voigt', 'number': 23452354, 'submit': True, 'tariff': 'namaf_physio_2019'}, 'modifiers': ['9', '0', '0'], 'url': '/home/practice/Documents/Juschdus sei Praxissss/MOMENTUM _Justus2020/6June2020/6_1Justus Voigt', 'invoice_name': 'MOMENTUM /2020/6-1', 'date_invoice': ['14.06.2020'], 'data': {'password': 'sha256$VYUvIpBX$467e2d0d0300897743486c98bc639d3ea3c25d36bbb0efde4b7ce7dc5e4cd389', 'uuid_text': '39D47121-AB31-11EA-B5C9-0AE0AFC200E9', 'email': 'justus@gmail.com', 'title': '', 'first_name': 'Justus', 'second_name': 'Voigt', 'phone': '061234234', 'cell': '081342342', 'fax': '0613423', 'pob': 'POB 37 ', 'city': 'Oshakati', 'country': 'Namibia', 'bank_holder': 'Justus Voigt', 'bank_account': '3124123455555', 'bank_branch': '50000', 'bank': 'FNB Oshakati', 'practice_name': 'Juschdus sei Praxissss', 'practice_number': '23412334545', 'hpcna_number': 'HPC234234', 'qualification': 'Bachelor of Arts (PPE)', 'specialisation': 'ComScie (MA)'}}


    createTextInvoice(data['treatments'],
            data["treatment_list"],
            data["prices"],
            data["dates"],
            data["patient"],
            data["modifiers"],
            data["url"],
            data["invoice_name"],
            data["date_invoice"],
            data["data"])


if __name__ == '__main__':
    testing()
