import pytest
import prettyprinter

prettyprinter.install_extras()
pytest.register_assert_rewrite("tests.helpers")
