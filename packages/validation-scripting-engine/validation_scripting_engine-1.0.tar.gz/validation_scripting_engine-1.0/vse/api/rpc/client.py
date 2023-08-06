import xmlrpc.client
import json

request_body = {
    "data": "",
    "opts": "",
}


class ClientRequest:

    def __init__(self, data, opts=None):
        self.data = data

        self.opts = opts if opts is not None else {}

    def to_dict(self):
        return {
            "data": self.data,
            "opts": self.opts,
        }


class VSERPCClient:
    def __init__(self, host="localhost", port=80):
        self._client = xmlrpc.client.ServerProxy(f'http://{host}/rpc/vse', allow_none=True)
        # self._client = xmlrpc.client.ServerProxy(f'http://{host}:{port}', allow_none=True)

    def get_methods(self):
        """
        Requests a list of supported methods on the server.

        """
        results = self._client.get_methods()
        return results

    def new_audit(self, data):
        """
        Generates new VSEAudit
        """
        results = self._client.new_audit(data)
        return results

    def run_audit(self, data):
        """
        Executes a New Audit based on JSON model.

        """
        req = ClientRequest(data)

        results = self._client.run_audit(req)
        return results

    def make_vse_task(self, data):
        """
        Generates new VSEAudit
        """
        results = self._client.make_vse_task(data)
        return results


if __name__ == "__main__":
    pass
