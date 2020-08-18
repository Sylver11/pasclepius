from flask_login import UserMixin

class User(UserMixin):

    def __init__(self, id, first_name='', uuid='', practice_uuid='',
            practice_name='', invoice_layout = '', active=True):
        self.uuid = uuid
        self.first_name = first_name
        self.practice_uuid = practice_uuid
        self.practice_name = practice_name
        self.invoice_layout = invoice_layout
        self.id = id
        self.active = active
    pass

