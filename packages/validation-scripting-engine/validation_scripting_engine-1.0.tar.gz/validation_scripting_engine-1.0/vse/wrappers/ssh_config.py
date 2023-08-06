import ipaddress

from marshmallow import Schema, fields, post_load, validates, ValidationError

from vse.core.constants import DEVICE_TYPES
from vse.wrappers import WrapperResult
from vse.wrappers.ssh_cmd import SSHCMDWrapper

NODE_TYPE_CONFIG_CMD_MAP = {
    "cisco_ios": "show running-config"
}


class SSHConfigWrapper(SSHCMDWrapper):

    def __init__(self, **kwargs):
        nodeType = kwargs.get("nodeType", "cisco_ios")
        if nodeType not in DEVICE_TYPES:
            raise ValueError(f"Invalid nodeType choices: {DEVICE_TYPES}")

        # Preforms Running-Config command lookup based on nodeType
        cmd = NODE_TYPE_CONFIG_CMD_MAP.get(nodeType, "show running-config")

        super().__init__(**kwargs, cmd=cmd)

    def send(self):
        wrapper_result = self._send()
        if not isinstance(wrapper_result, WrapperResult):
            return WrapperResult(None, False, "Invalid Return Type Received from self._send().")

        return wrapper_result


class SSHConfigWrapperSchema(Schema):
    target = fields.String(required=True)
    nodeType = fields.String(required=True)
    username = fields.String(required=True)
    password = fields.String(required=True)

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
    def make_object(self, data, **kwargs):
        return SSHConfigWrapper(**data)


def dev():
    wrapper = SSHConfigWrapper(
        target="192.168.1.2",
        nodeType="cisco_ios",
        username="cisco",
        password="cisco",
    )

    wrapper.send()


if __name__ == "__main__":
    dev()
