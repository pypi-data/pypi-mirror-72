from abc import abstractmethod, ABC

from vse.core.maps import ACTION_MAP
from vse.handlers.base import HandlerResult, Handler
from vse.handlers import DefaultHandler
from vse.core.task import VSETask
from vse.core.exceptions import InvalidHandlerErr


class IMapper(ABC):

    @abstractmethod
    def get_handler(self, task: VSETask) -> Handler:
        pass


class VSEActionMapper(IMapper):

    def __init__(self):
        self.action_map = ACTION_MAP

    def get_handler(self, task: VSETask) -> Handler:
        """
        Queries the HandlerMap based on the VSETask.action param. If Action is not found, a default Handler
        is returned.

        """
        if isinstance(task, VSETask):
            action = self.action_map.get(task.action, self.action_map.get("default"))

            handler_class = action.get("handler")

            if issubclass(handler_class, DefaultHandler):
                raise InvalidHandlerErr(f"Invalid Handler, Supported Handlers: '{self.action_map.keys()}'")

            handler = handler_class(
                name=task.action,
                params=task.params,
                task=task,
                params_schema=action.get("params_schema")()
            )
            return handler

        raise InvalidHandlerErr("Invalid Type provided, Must be of type Handler()")
