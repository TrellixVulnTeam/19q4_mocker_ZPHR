#!/usr/bin/env python3

import argparse
from abc import ABC, abstractmethod


# ============================================================================


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


def with_logging(function):
    def wrapper(self, *args, **kwargs):
        print("mocker.py " + self.NAME + " ", end="")
        print(*[repr(arg) for arg in args], end="")
        print(*["=".join([key, repr(val)]) for key, val in kwargs.items()])
        return function(self, *args, **kwargs)
    return wrapper


# ============================================================================


class Initialise(MockerCommand):
    NAME = 'init'

    def add_parser_to(self, subparsers):
        parser = subparsers.add_parser(self.NAME)
        parser.add_argument('directory', type=str)
        parser.set_defaults(mocker_command=self)

    @with_logging
    def apply(self, directory):
        raise NotImplementedError()

    def __call__(self, args):
        directory = args.directory
        self.apply(directory=directory)


# ============================================================================


class Pull(MockerCommand):
    NAME = 'pull'

    def add_parser_to(self, subparsers):
        parser = subparsers.add_parser(self.NAME)
        parser.add_argument('image', type=str)
        parser.set_defaults(mocker_command=self)

    @with_logging
    def apply(self, image):
        raise NotImplementedError()

    def __call__(self, args):
        image = args.image
        self.apply(image=image)


# ============================================================================


class RemoveImage(MockerCommand):
    NAME = 'rmi'

    def add_parser_to(self, subparsers):
        parser = subparsers.add_parser(self.NAME)
        parser.add_argument('image_id', type=int)
        parser.set_defaults(mocker_command=self)

    @with_logging
    def apply(self, image_id):
        raise NotImplementedError()

    def __call__(self, args):
        image_id = args.image_id
        self.apply(image_id=image_id)


# ============================================================================


class Images(MockerCommand):
    NAME = 'images'

    def add_parser_to(self, subparsers):
        parser = subparsers.add_parser(self.NAME)
        parser.set_defaults(mocker_command=self)

    @with_logging
    def apply(self):
        raise NotImplementedError()

    def __call__(self, args):
        self.apply()


# ============================================================================


class Processes(MockerCommand):
    NAME = 'ps'

    def add_parser_to(self, subparsers):
        parser = subparsers.add_parser(self.NAME)
        parser.set_defaults(mocker_command=self)

    @with_logging
    def apply(self):
        raise NotImplementedError()

    def __call__(self, args):
        self.apply()


# ============================================================================


class Run(MockerCommand):
    NAME = 'run'

    def add_parser_to(self, subparsers):
        parser = subparsers.add_parser(self.NAME)
        parser.add_argument('image_id', type=int)
        parser.add_argument('command', type=str, nargs='+')
        parser.set_defaults(mocker_command=self)

    @with_logging
    def apply(self, image_id, command):
        raise NotImplementedError()

    def __call__(self, args):
        image_id = args.image_id
        command = args.command
        self.apply(image_id=image_id, command=command)


# ============================================================================


class Execute(MockerCommand):
    NAME = 'exec'

    def add_parser_to(self, subparsers):
        parser = subparsers.add_parser(self.NAME)
        parser.add_argument('container_id', type=int)
        parser.add_argument('command', type=str, nargs='+')
        parser.set_defaults(mocker_command=self)

    @with_logging
    def apply(self, container_id, command):
        raise NotImplementedError()

    def __call__(self, args):
        container_id = args.container_id
        command = args.command
        self.apply(container_id=container_id, command=command)


# ============================================================================


class Logs(MockerCommand):
    NAME = 'logs'

    def add_parser_to(self, subparsers):
        parser = subparsers.add_parser(self.NAME)
        parser.add_argument('container_id', type=int)
        parser.set_defaults(mocker_command=self)

    @with_logging
    def apply(self, container_id):
        raise NotImplementedError()

    def __call__(self, args):
        container_id = args.container_id
        self.apply(container_id=container_id)


# ============================================================================


class RemoveContainer(MockerCommand):
    NAME = 'rm'

    def add_parser_to(self, subparsers):
        parser = subparsers.add_parser(self.NAME)
        parser.add_argument('container_id', type=int)
        parser.set_defaults(mocker_command=self)

    @with_logging
    def apply(self, container_id):
        raise NotImplementedError()

    def __call__(self, args):
        container_id = args.container_id
        self.apply(container_id=container_id)


# ============================================================================


class Commit(MockerCommand):
    NAME = 'commit'

    def add_parser_to(self, subparsers):
        parser = subparsers.add_parser(self.NAME)
        parser.add_argument('container_id', type=int)
        parser.add_argument('image_id', type=int)
        parser.set_defaults(mocker_command=self)

    @with_logging
    def apply(self, container_id, image_id):
        raise NotImplementedError()

    def __call__(self, args):
        container_id = args.container_id
        image_id = args.image_id
        self.apply(container_id=container_id, image_id=image_id)


# ============================================================================


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


# ============================================================================


def get_argparser():
    parser = argparse.ArgumentParser(
        description='Docker Python implementation')
    subparsers = parser.add_subparsers(title="mocker_commands")

    empty_mocker_command_error_message = \
        "mocker.py: error: no mocker_command given, printing help\n"
    parser.set_defaults(mocker_command=Help(parser, empty_mocker_command_error_message))

    mocker_commands = [
        Initialise(),
        Pull(),
        RemoveImage(),
        Images(),
        Processes(),
        Run(),
        Execute(),
        Logs(),
        RemoveContainer(),
        Commit(),
        Help(parser),
    ]

    for mocker_command in mocker_commands:
        mocker_command.add_parser_to(subparsers)

    return parser


if __name__ == "__main__":
    try:
        main_parser = get_argparser()
        main_args = main_parser.parse_args()
        main_args.mocker_command(main_args)
    except NotImplementedError:
        print("Not Implemented")


# ============================================================================

