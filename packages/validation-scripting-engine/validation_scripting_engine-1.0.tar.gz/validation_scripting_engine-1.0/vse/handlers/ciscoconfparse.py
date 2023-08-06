import ciscoconfparse

from vse.handlers import Handler, HandlerResult
from vse.handlers.schemas.ciscoconfparse import FindLinesParamSchema


class FindLinesHandler(Handler):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def execute(self, **kwargs) -> HandlerResult:

        config = None

        line_spec = self.params.get("line_spec")
        config_line_str = self.params.get("config_str_list")
        config_file_name = self.params.get("config_file_name")

        if config_line_str:
            config = config_line_str

        if config_file_name:
            config = config_file_name

        parser = ciscoconfparse.CiscoConfParse(config)
        results = parser.find_lines(line_spec)
        if len(results) > 0:
            self.result.msg = f'Matches: {results}'
            self.result.status = True
        else:
            self.result.msg = f'No Matches Detected'
            self.result.status = False

        self.check_expectation()

        return self.result
