from datetime import date
import calendar
import os


class InvoicePath(object):

    def __init__(self, medical_aid, patient_name, index, first_name, practice_name):
        self.today = date.today()
        self.medical_aid = medical_aid.strip()
        self.patient_name = patient_name.strip()
        self.index = index
        self.first_name = first_name.strip()
        self.practice_name = practice_name.strip()

   # def convert(self):
   #     self.date  =  datetime.strptime(self.date, '%d.%m.%Y')
   #     return self.date

    def date_digits(self, date_component):
        if date_component == 'year':
            return self.today.year
        elif date_component == 'month':
            return self.today.month
        elif date_component == 'day':
            return self.today.day

    def generate(self):
        self.path = os.getenv("INVOICE_URL") +'/'+ self.practice_name + '/' + str(self.medical_aid).upper() + '_' + self.first_name + str(self.date_digits('year')) + '/' + str(self.date_digits('month')) + calendar.month_name[self.date_digits('month')] + str(self.date_digits('year')) + '/' + str(self.date_digits('month')) + '_' + str(self.index) + self.patient_name
        return self.path

