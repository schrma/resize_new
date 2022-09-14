import os
import shlex

import pytest

import resize_new


@pytest.mark.parametrize("command_arg", ("--version", "--help", "-h"))
def test___argparse_version_help___no_error_raised(command_arg):
    command_line = command_arg
    input_parameter = shlex.split(command_line, posix=os.name == "posix")

    with pytest.raises(SystemExit) as pytest_wrapped_e:
        resize_new.main.main.parse_command_line_args(input_parameter)

    assert pytest_wrapped_e.value.code == 0
