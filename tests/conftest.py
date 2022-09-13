import os
import inspect
from collections import namedtuple

import pytest

TestFolders = namedtuple("TestFolders", ["input", "output"])
CURRENT_DIR = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))


@pytest.fixture(name="test_folder")
def test_folder_fixture():
    folders = TestFolders(os.path.join(CURRENT_DIR, "input_data"),
                          os.path.join(CURRENT_DIR, "output_data"))
    for folder in filter(lambda f: not os.path.exists(f), folders):
        os.makedirs(folder)
    return folders