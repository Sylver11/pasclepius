from datetime import date
import calendar
import os

class InvoiceName(object):

    def __init__(self, medical_aid, index, modifier):
        self.today = date.today()
        self.medical_aid = medical_aid.strip()
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
            return self.today.year
        elif date_component == 'month':
            return self.today.month

    def generate(self):
       # self.date = self.convert()
        self.invoice_id = str(self.medical_aid).upper() +'/' + str(self.date_digits('year')) + '/' + str(self.modifier) + str(self.date_digits('month')) + '-' + str(self.index)  
        return self.invoice_id


#patient = {'case': 'asdfasdfa',
#          'csrf_token':'ImU5NjFiYWEwN2Y1MGUyMmFiZDBkY2ZiYTQ5NDgxYzdiN2NlODQ2MDQi.XpVy6A.zOXe-xkr0gUZJroWUQHqVEoGxu0','date':
#          '14.04.2020', 'medical_aid': 'psemas', 'name': 'lotharrrr hoo', 'po':
#          '423423423#'}
#date = InvoiceName(patient, 3, ['14','0'])
#date_convert = date.generate()


