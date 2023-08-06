from datetime import datetime

from marshmallow import Schema, post_load, fields

from vse.core.mapping_agent import VSEActionMapper
from vse.handlers.base import HandlerResult, Handler
from vse.core.task import VSETask
from vse.core.audit import VSEAudit
from env import MAX_FAIL_LIMIT


class VSEResult:
    def __init__(self, audit: VSEAudit, **kwargs):
        """
        Use to represent the execution of a completed Audit. This object is return when the VSE.run() method
        has executed successfully. This object contains collections for both failed and successful task in the form of
        a HandlerResult for each task that was in the Audit.

        """
        self.audit = audit

        self.time_start = kwargs.get("time_start")
        self.audit_desc = kwargs.get("audit_desc")
        self.expectation_met = kwargs.get("expectation_met")
        self.success_task = kwargs.get("success_task", [])
        self.fail_task = kwargs.get("fail_task", [])
        self.MAX_FAIL_LIMIT = kwargs.get("fail_limit", MAX_FAIL_LIMIT)

    def to_dict(self):
        return {
            "expectation_met": self.expectation_met,
            "success_task": self.success_task,
            "fail_task": self.fail_task,
            "max_fail_limit": self.MAX_FAIL_LIMIT,

        }

    def __repr__(self):
        return f"<app.vse.VSEResult(audit_name={self.audit.name}, expectation_met={self.expectation_met})>"


class VSE:

    def __init__(self, **kwargs):
        """
        Validation Scripting Engine used to execute audits for the system.
        This is the core class used

        """

        self.audits = []
        self.mapper = VSEActionMapper()
        self.results = []

    def run(self) -> list:
        """
        Iterates over list of audits and executes each tasks.
        """

        for audit in self.audits:
            audit_result = VSEResult(audit=audit)
            audit_result.time_start = datetime.now()
            audit_result.MAX_FAIL_LIMIT = audit.fail_limit

            if audit.has_task():
                for task in audit.tasks:
                    handler = self.get_task_handler(task)

                    h_result = handler.execute()
                    if h_result.status == task.expectation:
                        audit_result.success_task.append(h_result.to_dict())

                    else:
                        audit_result.fail_task.append(h_result.to_dict())

                if len(audit_result.fail_task) > audit.fail_limit:
                    audit_result.expectation_met = False


                else:
                    audit_result.expectation_met = True

                self.results.append(audit_result)

        return self.results

    def get_task_handler(self, task: VSETask) -> Handler:
        """
        Gets Handler for the VSETask.
        """

        if isinstance(task, VSETask):
            handler = self.mapper.get_handler(task)
            return handler

        raise Exception("Invalid Type Provided, Must be of type VSETask")

    def add_audit(self, audit: VSEAudit) -> bool:
        """
        Adds Audit to VSE.audits collection.
        """
        if isinstance(audit, VSEAudit):
            self.audits.append(audit)
            return True

        return False

    def remove_audit(self, audit: VSEAudit) -> bool:
        """
         removes Audit from VSE.audits collection.
        """
        if isinstance(audit, VSEAudit):
            if audit in self.audits:
                index = self.audits.index(audit)
                self.audits.pop(index)
                return True

        return False

    def show_results(self):
        res = []
        if len(self.results) > 0:
            for audit_result in self.results:
                res.append(audit_result.to_dict())
        return res


class VSESchema(Schema):
    targets = fields.List(fields.String(), required=True)
    controlID = fields.String(required=True)
    description = fields.String(default="")
    expectation_limit = fields.Int(default=0)

    @post_load
    def make_vse(self, data, **kwargs):
        """
        Args:
            data:
            **kwargs:
        """
        return VSE(**data)


def main():
    __aurthur__ = "Courtney Baxter Jr"
    DESCRIPTION = \
        '''
        Validation Scripting Engine(VSE) is the validation tool used to automate control compliance based on intended
        expectations. 


        '''


if __name__ == "__main__":
    main()
