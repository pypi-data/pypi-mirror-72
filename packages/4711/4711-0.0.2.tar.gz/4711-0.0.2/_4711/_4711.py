import datetime
import inspect
import operator
import os
import platform
import re
import sys
from functools import reduce

from .__version__ import __version__


def cli(argv=None):
    if argv is None:
        argv = sys.argv
        if argv[0].endswith("pytest"):  # pragma: no cover
            argv = ["4711"]

    process_name = str(argv[0]) if argv and isinstance(argv, list) and len(argv) >= 1 else "4711"
    argv = argv[1:] if argv and isinstance(argv, list) and len(argv) > 1 else []
    if argv:
        argv = list(
            filter(lambda x: x.strip(), map(lambda x: x.strip(), reduce(operator.concat, [x.split("=") for x in argv])))
        )

    command = None
    optioned_command = None
    available_commands = ("help", "version")
    available_pre_command_options = {
        "-h": {"command": "help", "option": "--help", "values": 0},
        "--help": {"command": "help", "option": "--help", "values": 0},
        "-v": {"command": "version", "option": "--version", "values": 0},
        "-V": {"command": "version", "option": "--version", "values": 0},
        "--version": {"command": "version", "option": "--version", "values": 0},
    }

    option_values = []
    values = []
    value_count = 0
    for i, arg in enumerate(argv):
        if value_count:
            values.append(arg)
            value_count -= 1
            if value_count == 0:
                option_values.append(values)

        if command:
            break

        if arg in available_pre_command_options:
            info = available_pre_command_options[arg]

            if not optioned_command and info.get("command"):
                optioned_command = info.get("command")
            elif optioned_command and info.get("command") and info.get("command") != optioned_command:
                print("Something went wrong - conflicting options and/or commands")
                sys.exit(1)

            value_count = info.get("values")
            values = [info.get("option")]
            continue
        elif arg not in available_pre_command_options and arg.startswith("-"):
            print(f"Something went wrong - invalid option: {arg}")
            sys.exit(1)
        elif arg in available_commands:
            if optioned_command and optioned_command != arg:
                print("Something went wrong - conflicting options and/or commands")
                sys.exit(1)

            command = arg

    if not command:
        command = optioned_command or "help"

    if command == "help":
        print("Usage: 4711 [options] <command> [...]")
        print("")
        print("Options:")
        print("  -v, --version          print installed 4711 version")
        print("  -h, --help             show this help message and exit")
        sys.exit(0)

    if command == "version":
        cli_version = f"CLI: 4711 / version {__version__}"
        script_dir = os.path.dirname(inspect.stack()[-1][1])
        if script_dir and process_name and process_name.startswith(script_dir):
            cli_version = f'{cli_version} [exec: "{process_name}"]'
        print(cli_version)

        system_name = platform.uname().system
        if system_name == "Darwin":
            system_name = f"macOS {platform.mac_ver()[0]}"
        platform_line = f"Platform: {system_name} [{platform.machine()}]"
        print(platform_line)

        sys_version = re.sub(r"\s+", " ", sys.version)
        if sys_version.startswith(f"{platform.python_version()} "):
            version_len = len(platform.python_version())
            sys_version = sys_version[version_len:].strip()
        python_line = f"Python: {platform.python_version()} -- {sys_version}"
        if len(python_line) > 77:
            python_line = re.sub(r"(\[[^(]+) \([^)]+\)(.*)\]$", "\\1\\2]", python_line)
        if len(python_line) > 77:
            python_line = re.sub(r"[ .]+$", "", python_line[0:74])
            python_line = f"{python_line}..."
            if (python_line[::-1] + "[").index("[") < (python_line[::-1] + "]").index("]"):
                python_line = f"{python_line}]"
        print(python_line)

        print("")
        print(f"Timestamp (now): {datetime.datetime.utcnow().isoformat()}Z")
        sys.exit(0)


if __name__ == "__main__":  # pragma: no cover
    cli()  # pylint: disable=no-value-for-parameter
