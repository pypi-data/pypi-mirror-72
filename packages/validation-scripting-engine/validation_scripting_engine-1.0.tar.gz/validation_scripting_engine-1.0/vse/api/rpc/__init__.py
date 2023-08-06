import logging
from xmlrpc.server import SimpleXMLRPCServer
from xmlrpc.server import SimpleXMLRPCRequestHandler
from env import DEPLOY_MODE
from base64 import b64decode
from vse.core.audit import new_audit
from vse.api.rpc.services.vse import ServiceVSE

if DEPLOY_MODE == "dev":
    logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')


class RequestHandler(SimpleXMLRPCRequestHandler):
    rpc_paths = ('/RPC2',)

    def authenticate(self, headers):
        try:
            (basic, _, encoded) = headers.get('Authorization').partition(' ')


        except:
            print("No Auth")
            # Client did not ask for authentication
            return 1
        else:
            print("Auth")

            # Client authentication
            (basic, _, encoded) = headers.get('Authorization').partition(' ')
            assert basic == 'Basic', 'Only basic authentication supported'
            #    Encoded portion of the header is a string
            #    Need to convert to bytestring
            encodedByteString = encoded.encode()
            #    Decode Base64 byte String to a decoded Byte String
            decodedBytes = b64decode(encodedByteString)
            #    Convert from byte string to a regular String
            decodedString = decodedBytes.decode()
            #    Get the username and password from the string
            (username, _, password) = decodedString.partition(':')
            #    Check that username and password match internal dictionary
            print("Username: %s" % username)
            print("Password: %s" % password)
            if username == 'bibi' and password == 'bobo':
                return 1
            else:
                return 0

    def log_message(self, format, *args):
        # sys.stdout.write("%s - - [%s] %s\n" %
        #                  (self.address_string(),
        #                   self.log_date_time_string(),
        #                   format % args))

        logging.info(f"{self.address_string()}, {self.log_date_time_string()} {args}")


class VSERPCServer:

    def __init__(self, bind_ip="0.0.0.0", bind_port=8000):
        self.bind_ip = bind_ip
        self.bind_port = bind_port

        self._server = SimpleXMLRPCServer

    def run(self, debug=False):
        if debug:
            logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(message)s')

        with self._server((self.bind_ip, self.bind_port),
                          requestHandler=RequestHandler, allow_none=True, logRequests=True) as server:
            server.register_introspection_functions()

            # Function Registration
            server.register_instance(ServiceVSE())
            server.register_function(new_audit)

            logging.info(f"Running RPC Server: {server.server_address}")
            server.register_multicall_functions()

            server.serve_forever()


if __name__ == "__main__":
    server = VSERPCServer()

    server.run(True)
