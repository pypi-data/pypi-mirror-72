from vse.api.rpc.services.schemas import RPCResponse


class BaseService:

    def get_methods(self):
        """Returns a List of Methods"""
        resp = RPCResponse()

        resp.update(
            data=[attr for attr in self.__dir__() if attr.find("__")],
            msg="Available Methods Provided",
            status=True
        )
        return resp
