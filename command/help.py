from .mocker_command import MockerCommand
from .utils import with_logging


class Help(MockerCommand):
    NAME = 'help'

    def __init__(self, parser_to_print_help_of, additional_message=None):
        if additional_message is None:
            additional_message = ""

        self.parser_to_print_help_of = parser_to_print_help_of
        self.additional_message = additional_message

    def add_parser_to(self, subparsers):
        parser = subparsers.add_parser(self.NAME)
        parser.set_defaults(mocker_command=self)

    @with_logging
    def apply(self):
        self.parser_to_print_help_of.print_help()

    def __call__(self, args):
        if self.additional_message:
            print(self.additional_message)
        self.apply()
