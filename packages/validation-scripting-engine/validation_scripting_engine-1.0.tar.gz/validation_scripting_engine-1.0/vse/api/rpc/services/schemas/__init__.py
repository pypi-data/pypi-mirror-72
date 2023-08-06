from marshmallow import Schema, fields


class RPCRequest(Schema):
    data = fields.Dict(default={})
    opts = fields.Dict(default={})


class RPCResponse:

    def __init__(self, data=None, status=False, msg=""):
        self.msg = msg
        self.data = data
        self.status = status

    def update(self, **kwargs):
        self.msg = kwargs.get("msg")
        self.data = kwargs.get("data")
        self.status = kwargs.get("status")

