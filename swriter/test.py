from main import createTextInvoice

def testing():


    data = {"user":
            {"uuid_text": "00D70FBC-CD89-11EA-B445-15AE28BB36DA",
                "email": "justus@gmail.com",
                "title": "Dr",
                "first_name": "Justus ",
                "second_name": "Voigt",
                "phone": "",
                "cell": "0812342234",
                "fax": "",
                "pob": "PO Box 37",
                "city": "Oshakati",
                "country": "Namibia",
                "bank_holder": "DR J Voigt",
                "bank_account": "234234324",
                "bank_branch": "5000",
                "bank": "FNB Oshakati",
                "practice_name":
                "Justus's praxis",
                "practice_number": "2343242",
                "hpcna_number": "HPCN34223",
                "qualification": "BA PPE Bachelor ",
                "specialisation": "Specialist of po",
                "invoice_layout": 1},
            "invoice": {"csrf_token": "IjZhOWQ2NmY2NDU4YTBkMWNhZGY5YWM4OWRiOGFiM2M4NDAyMTcyMmEi.XyGgMg.dBFgyPCziGDSLUsGpNlCCUCLEGU",
                "date_invoice": "29.07.2020",
                "treatments": "501",
                "description": "Small bones",
                "units": "12800",
                "post_value": "2291.6",
                "value": "2291.6",
                "date": "14.07.2020",
                "medical_aid": "mva",
                "patient_name": "George Fischer",
                "case_number": "2342342",
                "po_number": "2433",
                "tariff": "namaf_orthopaedic_surgeons_2020",
                "date_created": "08.07.2020"},
            "treatments": ["501", "1333",  "774"],
            "descriptions": ["Small bones", "Ebstein's Anomaly","Repair of Boutonniere deformity or Mallet finger"],
            "units": ["12800", "56300", "12200"],
            "post_values": ["2291.6", "10079.6", "2184.2"],
            "dates": ["14.07.2020", "30.07.2020", "16.07.2020"],
            "invoice_file_url": "/Users/justus/Documents/Justus's praxis/MVA_Justus2020/7July2020/7_13George Fischer",
            "invoice_id": "MVA/2020/7-13"}

    createTextInvoice(
            data["user"],
            data["invoice"],
            data["invoice_id"],
            data["invoice_file_url"],
            data["treatments"],
            data["descriptions"],
            data["units"],
            data["post_values"],
            data["dates"],
            )


if __name__ == '__main__':
    testing()
