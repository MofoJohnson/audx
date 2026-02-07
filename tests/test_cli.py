import unittest
from unittest.mock import MagicMock, patch

from typer.testing import CliRunner

import audx.main
from audx import app

runner = CliRunner()


class TestCLI(unittest.TestCase):
    def test_invalid_path(self):
        with patch("audx.main.Path.is_dir", return_value=False):
            path = "invalid_path"
            result = runner.invoke(app, [path])
            assert result.exit_code != 0
            assert f"Provided path '{path}' is not a directory." in result.output


if __name__ == "__main__":
    _ = unittest.main()
