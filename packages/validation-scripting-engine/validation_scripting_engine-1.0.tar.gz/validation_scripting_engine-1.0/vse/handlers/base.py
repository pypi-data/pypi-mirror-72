from abc import ABC, abstractmethod
from marshmallow import Schema
from vse.core.exceptions import ParamSchemaValidationError


class IHandlerResult(ABC):

    @abstractmethod
    def to_dict(self):
        pass


class IHandler(ABC):

    @abstractmethod
    def execute(self, **kwargs) -> IHandlerResult:
        pass


class HandlerResult(IHandlerResult):
    def __init__(self, **kwargs):
        self.status = kwargs.get("status", False)
        self.handler_name = kwargs.get("name", "")
        self.msg = kwargs.get("msg", "")
        self.expectation_met = kwargs.get("expectation_met", False)
        self.task = kwargs.get("task")

    def to_dict(self):
        return {
            "status": self.status,
            "name": self.handler_name,
            "msg": self.msg,
            "expectation_met": self.expectation_met,
            "task_desc": self.task.description,
            "task_params": self.task.params,
            "task_expectation": self.task.expectation
        }

    def __repr__(self):
        return f'<HandlerResult(name={self.handler_name}, status={self.status}, msg="{self.msg}, expectation_met="{self.expectation_met}")>'


class Handler(IHandler):
    def __init__(self, **kwargs):

        self.params = None
        self.result = HandlerResult()

        self.task = kwargs.get("task")
        self.name = kwargs.get("name", "")
        self.params_schema = kwargs.get("params_schema", Schema)
        self.opts_schema = kwargs.get("opts", Schema)
        self.target_data = kwargs.get("target_data")

        self.result.handler_name = self.name

        self._extract_params()
        self._prep_results()
        self.validate_params()

    def execute(self, **kwargs) -> HandlerResult:
        raise NotImplementedError

    def _extract_params(self):
        """
        Extracts the parameter information from the VSETask object.
        """
        if self.task:
            self.params = self.task.params
            return

        self.params = None

    def _prep_results(self):
        """
        Applies the VSETask to the HandlerResult.task var.
        """
        if self.task:
            self.result.task = self.task

    def validate_params(self):
        """
        Validates the Parameters provided
        """
        validation_res = self.params_schema.validate(self.params)
        if len(validation_res) == 0:
            return True

        raise ParamSchemaValidationError(f"Invalid Parameters Provided: {self.params_schema.validate(self.params)}")

    def check_expectation(self):
        """
        Checks if the HandlerResult.status   matches the VSETask.expectation. If so, update the
        HandlerResult.expectation_met variable to reflect if the Task failed or passed.

        """
        if self.result.status == self.task.expectation:
            self.result.expectation_met = True
        else:
            self.result.expectation_met = False
