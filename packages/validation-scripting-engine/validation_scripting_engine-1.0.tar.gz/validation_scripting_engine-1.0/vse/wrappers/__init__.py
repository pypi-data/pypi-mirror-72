class Wrapper:
    def __init__(self, **kwargs):
        self.result = None


class WrapperResult:
    def __init__(self, data: any, status: bool, msg: str):
        self.data = data
        self.status = status
        self.msg = msg

    def __dict__(self):
        return {
            "data": self.data,
            "status": self.status,
            "msg": self.msg

        }

    @staticmethod
    def new(result_data: dict):
        return WrapperResult(
            data=result_data.get("data"),
            status=result_data.get("status"),
            msg=result_data.get("msg")
        )

    def to_dict(self):
        return self.__dict__()
