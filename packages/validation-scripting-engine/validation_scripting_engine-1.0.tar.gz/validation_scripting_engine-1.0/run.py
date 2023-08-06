import sys
from pathlib import Path


import argparse
from vse.api.rpc import VSERPCServer
from vse.api.rest import run_rest_server
from env import DEPLOY_MODE


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='VSE-CLI Tool')
    parser.add_argument('--serve_rpc',
                        action='store_true',
                        help="Starts the VSE XMLRPC API server."
                        )

    parser.add_argument('--serve_rest',
                        action='store_true',
                        help="Starts the VSE RESTFul API server."
                        )

    args = parser.parse_args()

    if args.serve_rpc:
        s = VSERPCServer()
        if DEPLOY_MODE == "dev":
            s.run(debug=True)
        else:
            s.run()

        print("it works")
    elif args.serve_rest:
        run_rest_server()
    else:
        parser.print_help()