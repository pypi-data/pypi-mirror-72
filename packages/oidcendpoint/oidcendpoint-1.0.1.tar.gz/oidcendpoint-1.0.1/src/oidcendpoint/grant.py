from oidcmsg.message import Message
from oidcmsg.message import OPTIONAL_LIST_OF_STRINGS
from oidcmsg.message import SINGLE_OPTIONAL_JSON
from oidcmsg.message import SINGLE_OPTIONAL_STRING


class GrantMessage(Message):
    c_param = {
        'scope': SINGLE_OPTIONAL_STRING,
        'authorization_details': SINGLE_OPTIONAL_JSON,
        'claims': SINGLE_OPTIONAL_JSON,
        'resources': OPTIONAL_LIST_OF_STRINGS
    }

class Grant:
    def __init__(self):
        pass

    def create(self):
        pass

    def update(self):
        pass

    def replace(self):
        pass

    def revoke(self, item):
        pass

    def query(self, item):
        pass