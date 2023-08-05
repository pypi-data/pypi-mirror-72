from legimens.helpers.AttrDict import AttrSubscrDict
from legimens.helpers.dictMap import obj_map

import json

def ref(o):
    return f"Legi_{hex(id(o))}"

class Object(AttrSubscrDict):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def _ref(self):
        return ref(self)

    def _prepare_send(self, name, value):
        return name, serial(value)

    def _commit_update(self, name, value):
        self[name] = value

    def _get_child_obj(self):
        # TODO: not used, should I keep it?
        children = []
        def _app(o):
            if isinstance(o, Object):
                children.append(o)
        for k in self:
            obj_map(self[k], pre=_app)
        return children

def serial(obj):
    def _tostr(o):
        if isinstance(o, Object):
            return ref(o)

    x = obj_map(obj, _tostr)
    #x = json.dumps(x)
    return x

