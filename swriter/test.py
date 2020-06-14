def testing():
    patient = {'case': 'asdfasdfa', 'csrf_token':'ImU5NjFiYWEwN2Y1MGUyMmFiZDBkY2ZiYTQ5NDgxYzdiN2NlODQ2MDQi.XpVy6A.zOXe-xkr0gUZJroWUQHqVEoGxu0','date': '2020-04-14', 'medical': 'mva', 'name': 'todayyy', 'po': '423423423'}
    dates = ['01-04-2020', '04-04-2020', '10-04-2020', '15-04-2020']
    treatments = [{'description': 'Infra-red, Radiant heat, Wax therapy Hot packs', 'units': 10, 'value': 98}, {'description': 'Infra-red, Radiant heat, Wax therapy Hot packs', 'units': 10, 'value': 98}, {'description': 'Infra-red, Radiant heat, Wax therapy Hot packs', 'units': 10, 'value': 98}, {'description': 'Infra-red, Radiant heat, Wax therapy Hot packs', 'units': 10, 'value': 98}]
    items = ['001', '001', '001', '001']
    price = ['300.45','435.25', '196', '444']
    modifier = ['0','0','0','14']
    url ='some/weird/url'
    invoice_name = 'soemwierdname'
    createTextInvoice(items, treatments, price, dates, patient, modifier, url,
                     invoice_name)

if __name__ == '__main__':
    testing()
