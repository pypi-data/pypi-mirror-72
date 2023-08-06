import json
from marshmallow import Schema, post_load, fields, validates, ValidationError
import requests
import ipaddress
from vse.core.constants import JSON_RESPONSE_HEADERS, DEVICE_TYPES
from env import SSH_ENDPOINT, CONNECTOR_URL
from vse.wrappers import Wrapper, WrapperResult



class SSHCMDWrapper(Wrapper):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.target = kwargs.get("target")
        self.nodeType = kwargs.get("nodeType", "cisco_ios")
        self.username = kwargs.get("username")
        self.password = kwargs.get("password")
        self.cmd = kwargs.get("cmd")

        self.data = None
        self.ssh_endpoint = SSH_ENDPOINT

    def send(self):
        return self._send()

    def _send(self) -> WrapperResult:
        """
        sends post request to the connectors ssh service. If server timeout occurs,
        returns WrapperResult with False status.

        :return:
        """
        body = {
            "target": self.target,
            "nodeType": self.nodeType,
            "username": self.username,
            "password": self.password,
            "cmd": self.cmd
        }
        try:
            result = requests.post(self.ssh_endpoint, json=body, headers=JSON_RESPONSE_HEADERS)

            if result.status_code == 200:
                cmd_results = result.json().get("data")
                return WrapperResult(cmd_results, True, "Successful")

            if result.status_code == 400:
                self.data = None
                return WrapperResult(
                    None,
                    False,
                    f"Unable to Execute Command: {self.cmd} on Target: {self.target}")
        except requests.Timeout as err:
            return WrapperResult(None, False, str(err))

        return WrapperResult(None, False, "Unknown Error Occurred")


class SSHCMDWrapperSchema(Schema):
    target = fields.String(required=True)
    nodeType = fields.String(required=True)
    username = fields.String(required=True)
    password = fields.String(required=True)
    cmd = fields.String(required=True)

    @validates("target")
    def validate_target(self, value):
        try:
            ipaddress.IPv4Address(value)
        except ipaddress.AddressValueError:
            raise

    @validates('nodeType')
    def validate_nodeType(self, value):
        if value not in DEVICE_TYPES:
            raise ValidationError(f"Invalid nodeType choices: {DEVICE_TYPES}")

    @post_load
    def load_wrapper(self, data, **kwargs):
        return SSHCMDWrapper(**data)


def dev():
    wrapper = SSHCMDWrapper(target="192.168.1.2", nodeType="cisco_ios", username="cisco", password="cisco",
                            cmd="show run")

    results = wrapper.send()

    print(results.status)


if __name__ == "__main__":
    dev()
