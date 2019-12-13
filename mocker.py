#!/usr/bin/env python3

import argparse

import command


def get_argparser():
    parser = argparse.ArgumentParser(
        description='Docker Python implementation')
    subparsers = parser.add_subparsers(title="mocker_commands")

    empty_mocker_command_error_message = \
        "mocker.py: error: no mocker_command given, printing help\n"
    empty_mocker_command = command.Help(
        parser, empty_mocker_command_error_message
    )
    parser.set_defaults(mocker_command=empty_mocker_command)

    mocker_commands = [
        command.Initialise(),
        command.Pull(),
        command.RemoveImage(),
        command.Images(),
        command.Processes(),
        command.Run(),
        command.Execute(),
        command.Logs(),
        command.RemoveContainer(),
        command.Commit(),
        command.Help(parser),
    ]

    for mocker_command in mocker_commands:
        mocker_command.add_parser_to(subparsers)

    return parser


if __name__ == "__main__":
    try:
        parser = get_argparser()
        args = parser.parse_args()
        args.mocker_command(args)
    except NotImplementedError:
        print("Not Implemented")
