import logging

from vse.core import VSE
from vse.core.audit import new_audit
from vse.api.rpc.services import BaseService
from vse.api.rpc.services.schemas import RPCRequest, RPCResponse


class ServiceVSERequest(RPCRequest):
    pass


class ServiceVSE(BaseService):

    @staticmethod
    def run_audit(rpc_req):
        req_schema = RPCRequest()
        resp = RPCResponse()

        if len(req_schema.validate(rpc_req)) > 0:
            # Implement Error Handle Code
            raise Exception("Invalid Request")

        data = rpc_req.get("data")

        vse = VSE()

        audit = new_audit(data)
        vse.add_audit(audit)
        results = vse.run()

        MSG = f"Completed Audit for Target: '{audit.target}' Passed: {results[0].expectation_met}"

        resp.update(data=results, status=True, msg=MSG)

        logging.info(MSG)
        return resp
