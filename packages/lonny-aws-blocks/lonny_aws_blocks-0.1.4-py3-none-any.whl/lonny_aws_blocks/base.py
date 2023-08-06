from base64 import b32encode
from lonny_aws_blob import Blob, query
import json

UPDATE_STATUS = "update"
DESTROY_STATUS = "destroy"
STABLE_STATUS = "stable"

PARAMS_FIELD = "__params__"
RESULT_FIELD = "__result__"
STATUS_FIELD = "__status__"
RESOURCE_TYPE_FIELD = "__resource_type__"
TAG_PREFIX = "__tag__"

_constructor_registry = dict()

def register(cls):
    _constructor_registry[cls.resource_type] = cls
    return cls

def constructor(resource_type):
    return _constructor_registry[resource_type]

class Resource:
    def get_name(self):
        tags = self.get_tags()
        parts = (tags[k] for k in sorted(tags.keys()))
        encoded = (b32encode(x.encode("utf-8")).decode("utf-8").strip("=").lower() for x in parts)
        return "-".join(["blocks", self.__class__.resource_type.value, *encoded])

    def update(self, *args, **kwargs):
        blob = Blob(self.get_name())
        blob.update(**{
            STATUS_FIELD : UPDATE_STATUS,
            PARAMS_FIELD : json.dumps([args, kwargs]),
            RESOURCE_TYPE_FIELD : self.__class__.resource_type.value,
            ** { f"{TAG_PREFIX}{k}" : v for k,v in self.get_tags().items() }
        })
        result = self.on_update(*args, **kwargs)
        blob.update(**{
            STATUS_FIELD : STABLE_STATUS,
            RESULT_FIELD : json.dumps(result)
        })
        return self.get_data()

    def destroy(self):
        blob = Blob(self.get_name())
        blob.update(**{ 
            STATUS_FIELD : DESTROY_STATUS
        })
        self.on_destroy()
        blob.destroy()

    def get_data(self):
        data = Blob(self.get_name()).get()
        if data.get(STATUS_FIELD) != STABLE_STATUS:
            raise RuntimeError(f"Resource: {self} not stable")
        return json.loads(data[RESULT_FIELD])

    def on_update(*args, **kwargs):
        pass

    def on_destroy(self):
        pass

    def get_tags(self):
        return dict()

    def __str__(self):
        payload = ",".join(f"{k}={v}" for k,v in self.get_tags().items())
        return f"{self.__class__.resource_type.name}({payload})"

    @classmethod
    def search(cls, ** tags):
        blobs = query( ** {
            RESOURCE_TYPE_FIELD : cls.resource_type.value,
            ** { f"{TAG_PREFIX}{k}" : v for k,v in tags.items() }
        })
        for blob in blobs:
            tags = { k[len(TAG_PREFIX):] : v for k,v in blob.get().items() if k.startswith(TAG_PREFIX) }
            yield cls.from_tags(tags)