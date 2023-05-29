import pytest
import unittest.mock as mock
import logging
from {{cookiecutter.project_slug}}.app.utils.logging import StandardFormatter


class TestStandardFormatter:
    def test_build_msg_format(self):
        msg_format = StandardFormatter().build_msg_format()
        assert msg_format == "%(asctime)-22.19s %(name)-21s [%(levelname)s]:" \
                             "    %(message)s    (%(filename)s:%(lineno)d)"

    @pytest.mark.parametrize("level_no, level_name",
                             [(logging.DEBUG, "DEBUG"),
                              (logging.INFO, "INFO"),
                              (logging.WARNING, "WARNING"),
                              (logging.ERROR, "ERROR"),
                              (logging.CRITICAL, "CRITICAL")])
    @mock.patch("{{cookiecutter.project_slug}}.app.utils.logging.logging.Formatter")
    def test_format(self, mocked_formatter, level_no, level_name):
        mocked_formatter.return_value.format.return_value = "dummy return"
        record = mock.MagicMock(spec=logging.LogRecord,
                                levelno=level_no,
                                levelname=level_name,
                                name="dummy_logger")
        output = StandardFormatter().format(record)
        log_fmt = "%(asctime)-22.19s %(name)-21s [%(levelname)s]:    " \
                  "%(message)s    (%(filename)s:%(lineno)d)"
        mocked_formatter.assert_called_with(log_fmt)
        mocked_formatter.return_value.format.assert_called_with(record)
        assert output == "dummy return"