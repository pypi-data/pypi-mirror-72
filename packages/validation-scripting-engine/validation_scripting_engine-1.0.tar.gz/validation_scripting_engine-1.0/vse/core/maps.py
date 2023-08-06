from vse.handlers import BaseHandler, DefaultHandler
from vse.handlers.test import TestHandler
from vse.handlers.ciscoconfparse import FindLinesHandler
from vse.handlers.schemas.ciscoconfparse import FindLinesParamSchema
from vse.handlers.schemas import TestHandlerParams
from vse.handlers.schemas import DefaultHandlerParams

ACTION_MAP = {
    "h_find_lines": {
        "handler": FindLinesHandler,
        "params_schema": FindLinesParamSchema
    },
    "test_handler": {
        "handler": TestHandler,
        "params_schema": TestHandlerParams
    },
    "default": {
        "handler": DefaultHandler,
        "params_schema": DefaultHandlerParams
    }
}
