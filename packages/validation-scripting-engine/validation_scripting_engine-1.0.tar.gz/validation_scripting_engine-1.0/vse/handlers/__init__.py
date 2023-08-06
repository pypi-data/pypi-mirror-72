from vse.handlers.base import Handler, HandlerResult


class BaseHandler(Handler):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def execute(self, **kwargs) -> HandlerResult:
        self.result.status = False
        return self.result


class DefaultHandler(Handler):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def execute(self, **kwargs) -> HandlerResult:
        is_on = self.params

        if is_on:
            self.result.status = True
            self.result.msg = "Default Handler Executed"
        else:
            self.result.status = False
            self.result.msg = "Invalid Handler"

        self.check_expectation()
        return self.result
