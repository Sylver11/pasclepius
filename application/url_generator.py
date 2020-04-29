from datetime import datetime
from dotenv import load_dotenv
import calendar
import os

load_dotenv()


class InvoicePath(object):

    def __init__(self, date, medical):
        self.date = date
        self.medical = medical

    def convert(self):
        print(self.date)
        self.date  =  datetime.strptime(self.date, '%d.%m.%Y')
        return self.date

    def date_digits(self, date_component):
        if date_component == 'year':
            return self.date.year
        elif date_component == 'month':
            return self.date.month
        elif date_component == 'day':
            return self.date.day


    def generate(self, name):
       # date_component = self.date_digits(date_component)
        self.date = self.convert()
        self.path = os.getenv("OWNCLOUD_URL") +'/' + str(self.medical).upper() + '_' + os.getenv("USERNAME") + str(self.date_digits('year')) + '/' + str(self.date_digits('month')) + calendar.month_name[self.date_digits('month')] + str(self.date_digits('year')) + '/' + name


        return self.path
   # os.getenv("OWNCLOUD_URL") + 
   # os.getenv("SYSTEM_URL")
   # def patient(self, name):
   #     self.date 





date = InvoicePath('14.04.2020', 'mva')
#print(date)
date_convert = date.generate("Justus")

print(date_convert)


