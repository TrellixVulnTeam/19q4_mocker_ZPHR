from abc import ABC, abstractmethod


class MockerCommand(ABC):
    NAME = "UNKNOWN"

    @abstractmethod
    def add_parser_to(self, subparsers):
        pass

    @abstractmethod
    def apply(self, *args, **kwargs):
        pass

    @abstractmethod
    def __call__(self, args):
        pass
