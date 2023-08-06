from marshmallow import Schema, fields, post_load
from vse.core.task import VSETask, VSETaskSchema


def validate_tasks(task_list):
    schema = VSETaskSchema()
    for task in task_list:
        schema.validate(task)


class VSEAudit:
    def __init__(self, **kwargs):
        self.target = kwargs.get("target")
        self.name = kwargs.get("name")
        self.tasks = kwargs.get("tasks", [])
        self.target_facts = kwargs.get("target_facts")
        self.description = kwargs.get("description")
        self.fail_limit = kwargs.get("fail_limit")

    def add_task(self, task: VSETask) -> bool:
        """
        Adds VSETask to self.tasks list.
        """
        if isinstance(task, VSETask):
            if task not in self.tasks:
                self.tasks.append(task)
                return True

        return False

    def del_task(self, task: VSETask) -> bool:
        if task in self.tasks:
            _index = self.tasks.index(task)
            self.tasks.pop(_index)
            return True

        return False

    def clear_task(self) -> bool:
        if len(self.tasks) > 0:
            self.tasks = []
            return True

        return False

    def get_target_facts(self):
        # TODO: Implement method to get target facts.
        raise NotImplementedError

    def has_task(self):
        if len(self.tasks) == 0:
            return False
        else:
            return True

    def to_dict(self):
        return {
            "target": self.target,
            "tasks": [task.to_dict() for task in self.tasks],
            "target_facts": self.target_facts,
            "description": self.description,
            "fail_limit": self.fail_limit,
        }


class VSEAuditSchema(Schema):
    target = fields.String(required=True)
    tasks = fields.List(fields.Nested(VSETaskSchema()))
    target_facts = fields.Dict()
    description = fields.String(default="")
    fail_limit = fields.Int(default=0)

    @post_load
    def make_audit(self, data, **kwargs):
        return VSEAudit(**data)

    meta = {"collection": "vse_audits"}


def new_audit(data):
    """
    Generates a New VSEAudit based on dict.

    Params:
        target = fields.String(required=True)
        tasks = fields.List(fields.Dict())
        target_facts = fields.Dict()
        description = fields.String(default="")
        fail_limit = fields.Int(default=0)

    """
    model = VSEAuditSchema().load(data)
    return model
