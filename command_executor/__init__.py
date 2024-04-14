import argparse
import sys
from typing import Dict 

from command_executor.command_class_inspector import * 


def command_executor_main(cls):
    parser = argparse.ArgumentParser()
    available_commands = get_available_commands(cls)
    command_parsers = parser.add_subparsers(dest="command")

    commands: Dict[str, argparse.ArgumentParser] = {}
    for command in available_commands:
        commands[command] = command_parsers.add_parser(command)

        for arg in get_arguments(getattr(cls, command)):
            commands[command].add_argument("--%s" % (arg.replace("_", "-")), 
                required=True, 
                action="store", 
                type=get_arg_type(getattr(cls, command), arg),
                help=get_arg_description(getattr(cls, command), arg)
            )
        for arg, value in get_optional_arguments(getattr(cls, command)):
            if get_arg_type(getattr(cls, command), arg) == bool:
                    commands[command].add_argument("--%s" % (arg.replace("_", "-")), 
                    default=value,
                    action="store_const",
                    const=True,
                    help=get_arg_description(getattr(cls, command), arg)
                )
            else:
                commands[command].add_argument("--%s" % (arg.replace("_", "-")), 
                    default=value,
                    action="store",
                    type=get_arg_type(getattr(cls, command), arg),
                    help=get_arg_description(getattr(cls, command), arg)
                )


    args, _ = parser.parse_known_args()
    executor = cls()
    if hasattr(executor, args.command):
        m = getattr(executor, args.command)
        A = {}
        for arg in get_arguments(m):
            if arg != "self":
                A[arg] = getattr(args, arg)
        for arg, _ in get_optional_arguments(m):
            A[arg] = getattr(args, arg)
        result = m(**A)
        if isinstance(result, dict):
            # pretty print dict 
            for k,v in result.items():
                print("%s: %s" % (k, v))
        elif result is not None:
            print(result)
    else:
        print("This feature is not implemented yet")

