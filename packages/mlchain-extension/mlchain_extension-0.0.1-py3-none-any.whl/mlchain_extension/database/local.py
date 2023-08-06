from .base import MLDatabase
from uuid import uuid4

class LocalDatabase(MLDatabase):
    def __init__(self):
        MLDatabase.__init__(self)
        self.data = {}

    def insert(self, document, id=None, *args, **kwargs):
        if id is None:
            id = uuid4().hex
        self.data[id] = document

    def get(self, id, *args, **kwargs):
        print(id,self.data[id])
        return self.data.get(id)

    def update(self, id, document, *args, **kwargs):
        print(id,document)
        if id not in self.data:
            self.data[id] = document
        else:
            def __update(__doc, __key, __value):
                if __key in __doc:
                    if isinstance(__value, dict):
                        for k, v in __value.items():
                            __update(__doc[__key], k, v)
                    else:
                        __doc[__key] = __value
                else:
                    __doc[__key] = __value

            __update(self.data, id, document)
