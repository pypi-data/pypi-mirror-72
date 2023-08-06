import unittest
from vse.api.rpc.client import VSERPCClient
"""
WARNING: Test requires the auditor api service to run. If you need to execute the service, run the following command

docker run -p 8000:8000 -d cbaxter1988/auditor:api
"""

# HOST = "192.168.1.22"
HOST = "io.cbaxterjr.com"
# HOST = "localhost"
PORT = 80


class MyTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls.c = VSERPCClient(host=HOST, port=PORT)

    def test_get_methods(self):
        resp = self.c.get_methods()
        methods = resp.get("data")

        self.assertIsInstance(methods, list)

    def test_run_audit(self):
        data = {
            "target": "192.168.1.1",
            "description": "This is My Example Audit",
            "target_facts": {
                "assetHostname ": "r1.bits.local",
                "nodeType": "cisco_ios"
            },
            "fail_limit": 0,
            "tasks": [
                {
                    "action": "test_handler",
                    "description": "Executes the TestHandler",
                    "params": {
                        "poked": True
                    },
                    "expectation": True
                },
                {
                    "action": "h_find_lines",
                    "description": "Checks if hostname if configured on device, If Match Pass",
                    "params": {
                        "line_spec": "hostname (.*)",
                        "config_str_list": [
                            "hostname r1.bits.local"
                        ]
                    },
                    "expectation": True
                }
            ]
        }

        resp = self.c.run_audit(data)

        resp_data = resp.get("data")
        self.assertIsInstance(resp_data, list)



if __name__ == '__main__':
    unittest.main()
