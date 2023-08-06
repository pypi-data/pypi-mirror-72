from marshmallow import fields

from vse.handlers.schemas import ParamsSchema, OptsSchema


class CiscoConfParseSchema(ParamsSchema):
    config_str_list = fields.List(fields.String)
    config_file_name = fields.String()


class FindLinesParamSchema(CiscoConfParseSchema):
    line_spec = fields.String(required=True)
