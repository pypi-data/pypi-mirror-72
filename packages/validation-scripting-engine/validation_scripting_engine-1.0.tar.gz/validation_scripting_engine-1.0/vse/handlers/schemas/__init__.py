from marshmallow import Schema, fields


class OptsSchema(Schema):
    store = fields.Bool(default=False)


class ParamsSchema(Schema):
    pass


class DefaultHandlerParams(ParamsSchema):
    is_on = fields.Bool(default=False)


class TestHandlerParams(ParamsSchema, OptsSchema):
    poked = fields.Boolean(required=True)
