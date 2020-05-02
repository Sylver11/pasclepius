from datetime import datetime
import calendar
import os

class InvoiceName(object):

    def __init__(self, patient, index, modifier):
        self.date = patient['date']
        self.medical = patient['medical']
        self.index = index
        if '14' in modifier:
            self.modifier = 'H'
        else:
            self.modifier = ''

    def convert(self):
        self.date  =  datetime.strptime(self.date, '%d.%m.%Y')
        return self.date

    def date_digits(self, date_component):
        if date_component == 'year':
            return self.date.year
        elif date_component == 'month':
            return self.date.month

    def generate(self):
        self.date = self.convert()
        self.invoice_no = str(self.medical).upper() +'/' + str(self.date_digits('year')) + '/' + str(self.modifier) + str(self.date_digits('month')) + '-' + str(self.index)  
        return self.invoice_no


#patient = {'case': 'asdfasdfa',
#          'csrf_token':'ImU5NjFiYWEwN2Y1MGUyMmFiZDBkY2ZiYTQ5NDgxYzdiN2NlODQ2MDQi.XpVy6A.zOXe-xkr0gUZJroWUQHqVEoGxu0','date':
#          '14.04.2020', 'medical': 'psemas', 'name': 'lotharrrr hoo', 'po':
#          '423423423#'}
#date = InvoiceName(patient, 3, ['14','0'])
#date_convert = date.generate()
#print(date_convert)


