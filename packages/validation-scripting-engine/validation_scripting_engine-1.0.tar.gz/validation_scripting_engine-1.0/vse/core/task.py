from marshmallow import Schema, fields, post_load, ValidationError, validates
from vse.core.maps import ACTION_MAP


### VSETask Model ###
class VSETask:
    def __init__(self, **kwargs):
        self.action = kwargs.get("action", "default")
        self.expectation = kwargs.get("expectation", True)
        self.params = kwargs.get("params")
        self.description = kwargs.get("description")
        self.control_info = kwargs.get("control_info")

    def to_dict(self):
        return {
            "action": self.action,
            "description": self.description,
            "expectation": self.expectation,
            "params": self.params,
            "control_info": self.control_info
        }


class VSETaskSchema(Schema):
    action = fields.String(required=True)
    description = fields.String(default="")
    expectation = fields.Bool(default=True)
    params = fields.Dict(default={})
    control_info = fields.Dict(default={})

    @validates('action')
    def validate_action(self, action):
        actions = list(ACTION_MAP.keys())
        if actions.count(action) == 0:
            raise ValidationError(f'Invalid Action Provided, Options: {actions}')
        else:
            return False

    @post_load
    def make_task(self, data, **kwargs) -> VSETask:
        return VSETask(**data)


def make_vse_task(data) -> VSETask:
    return VSETaskSchema().load(data)


def dev():
    pass


if __name__ == "__main__":
    dev()
