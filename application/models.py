from flask_login import UserMixin

class User(UserMixin):

    def __init__(self, id, first_name='', uuid='', practice_uuid='',
            practice_name='', practice_id='', practice_admin='', invoice_layout = '', namaf_profession = '',
            practice_role='', active=True):
        self.uuid = uuid
        self.first_name = first_name
        self.practice_uuid = practice_uuid
        self.practice_name = practice_name
        self.practice_id = practice_id
        self.practice_admin = practice_admin
        self.invoice_layout = invoice_layout
        self.namaf_profession = namaf_profession
        self.practice_role = practice_role
        self.id = id
        self.active = active
    pass

