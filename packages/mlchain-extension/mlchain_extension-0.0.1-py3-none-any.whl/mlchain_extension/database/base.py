class MLDatabase:
    def insert(self, document, id=None, *args, **kwargs):
        raise NotImplementedError

    def get(self, id, *args, **kwargs):
        raise NotImplementedError

    def update(self, id, document, *args, **kwargs):
        raise NotImplementedError
