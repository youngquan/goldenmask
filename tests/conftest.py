import sys

import pytest


@pytest.fixture
def suffix_so_or_pyd():
    if sys.platform == "win32" or sys.platform == "cygwin":
        return ".pyd"
    else:
        return ".so"
