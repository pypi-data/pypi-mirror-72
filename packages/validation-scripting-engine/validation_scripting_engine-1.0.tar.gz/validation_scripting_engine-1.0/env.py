import os

DEPLOY_MODE = os.getenv("DEPLOY_MODE", "dev")

CONNECTOR_HOST = os.getenv("CONNECTOR_HOST", "192.168.1.104")
SSH_ENDPOINT = os.getenv("SSH_ENDPOINT", "http://192.168.1.104:5001/v1/ssh")
CONNECTOR_URL = os.getenv("CONNECTOR_URL", f"http://{CONNECTOR_HOST}/connector")

MAX_FAIL_LIMIT = os.getenv("MAX_FAIL_LIMIT", 0)
VSE_RPC_PORT = os.getenv("VSE_RPC_PORT", 8000)

VSE_REST_HOST = os.getenv("VSE_REST_HOST", "0.0.0.0")
VSE_REST_PORT = os.getenv("VSE_REST_PORT", 8070)