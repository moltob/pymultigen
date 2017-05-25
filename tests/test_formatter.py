import pytest

from multigen.formatter import format_raw, format_autopep8


@pytest.fixture
def ugly_code():
    return "import  a ,  b"


def test__format_raw(ugly_code):
    assert format_raw(ugly_code) is ugly_code


def test__format_pep8(ugly_code):
    assert format_autopep8(ugly_code) == "import a\nimport b\n"
