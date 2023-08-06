from vse.handlers import Handler, HandlerResult


class TestHandler(Handler):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def execute(self, **kwargs) -> HandlerResult:

        poked = self.params.get("poked", False)

        if poked:
            self.result.status = True
            self.result.msg = "Hey, You Poked Me"

        else:
            # print(self.params)
            self.result.status = False
            self.result.msg = "What do you want?"

        self.check_expectation()
        return self.result
