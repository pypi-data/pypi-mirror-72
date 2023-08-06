from bottle import route, response, request, run
from vse.core import VSE
from vse.core.audit import new_audit
from env import DEPLOY_MODE, VSE_REST_PORT, VSE_REST_HOST

import logging


def make_json_response(data, status):
    response.set_header("content-type", "application/json")
    response.body = data
    response.status = status
    return response.body


@route('/vse', method=['POST'])
def run_audit():
    if request.method == "POST":
        audit_data = request.json

        vse = VSE()

        audit = new_audit(audit_data)
        vse.add_audit(audit)
        results = vse.run()

        MSG = f"Completed Audit for Target: '{audit.target}' Passed: {results[0].expectation_met}"
        logging.info(MSG)
        response.status = 200
        response.body = results[0].to_dict()
        response.set_header("content-type", "application/json")

        return response.body


def run_rest_server():
    if DEPLOY_MODE == "dev":
        run(host=VSE_REST_HOST, port=VSE_REST_PORT, debug=True)
    else:
        run(host=VSE_REST_HOST, port=VSE_REST_PORT)


if __name__ == "__main__":
    if DEPLOY_MODE == "dev":
        run(host=VSE_REST_HOST, port=VSE_REST_PORT, debug=True)
    else:
        run(host=VSE_REST_HOST, port=VSE_REST_PORT)
