import os

from google.cloud import ndb
from google.cloud.ndb.exceptions import ContextError

class Settings(ndb.Model):
    name = ndb.StringProperty()
    value = ndb.StringProperty()

    @classmethod
    def get(cls, name):
        setting = cls.query(cls.name == name).get()
        print("hello")
        if not setting:
            setting = cls(name=name, value="UNSET")
            setting.put()
        
        return setting.value
