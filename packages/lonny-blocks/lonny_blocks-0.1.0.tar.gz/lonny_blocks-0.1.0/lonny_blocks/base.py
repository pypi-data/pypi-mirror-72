from base64 import b32encode
from lonny_aws_blob import Blob, query

sync_cache = dict()
cls_registry = dict()

def register(cls):
    cls_registry[cls.node_type] = cls
    return cls

def constructor(node_type):
    return cls_registry[node_type]

class Node:
    @property
    def name(self):
        parts = [self.__class__.node_type.name, *self.get_parts()]
        encoded = (b32encode(x.encode("utf-8")).decode("utf-8").strip("=").lower() for x in parts)
        return "-".join(encoded)

    def encode(self):
        return dict()

    def get_parts(self):
        return list()

    def sync(self, *, force = False):
        if self.name not in sync_cache or force:
            sync_cache[self.name] = self.on_sync()
        return sync_cache[self.name]

    def destroy(self):
        self.on_destroy()

    def on_sync(self):
        Blob(self.name).update(
            node_type = self.__class__.node_type.name,
            ** self.encode()
        )

    def on_destroy(self):
        Blob(self.name).destroy()

    @classmethod
    def search(cls, *, project = None, stage = None):
        for blob in query(dict(node_type = cls.node_type.name, project = project, stage = stage)):
            data = blob.get()
            yield cls.decode(data)

