import pytest
import unittest.mock as mock
import click
import logging
from {{cookiecutter.project_slug}}.app.utils.logging import ColorFormatter, request_msg_format


class TestColorFormatter:
    @pytest.mark.parametrize("log_level, color, expected_output", [
        (logging.DEBUG, "cyan", "\x1b[36mhello\x1b[0m"),
        (logging.INFO, "green", "\x1b[32mhello\x1b[0m"),
        (logging.WARNING, "yellow", "\x1b[33mhello\x1b[0m"),
        (logging.ERROR, "red", "\x1b[31mhello\x1b[0m"),
        (logging.CRITICAL, "bright_red", "\x1b[91mhello\x1b[0m")])
    @mock.patch("{{cookiecutter.project_slug}}.app.utils.logging.click.style",
                side_effect=click.style)
    def test_level_name_colors(self, mocked_click_style, log_level, color,
                               expected_output):
        dummy_input = "hello"
        dummy_output_func = ColorFormatter.level_name_colors[log_level]
        dummy_output = dummy_output_func(dummy_input)
        mocked_click_style.assert_called_with(dummy_input, fg=color)
        assert dummy_output == expected_output

    @pytest.mark.parametrize("levelno, expected_log_format",
                             [(0, "%(asctime)-22.19s \x1b[1m%(name)-21s\x1b[0m [\x1b[34m%(levelname)s\x1b[0m]:    %(message)s    (%(filename)s:%(lineno)d)"),
                              (10, "%(asctime)-22.19s \x1b[1m%(name)-21s\x1b[0m [\x1b[36m%(levelname)s\x1b[0m]:    %(message)s    (%(filename)s:%(lineno)d)"),
                              (20, "%(asctime)-22.19s \x1b[1m%(name)-21s\x1b[0m [\x1b[32m%(levelname)s\x1b[0m]:    %(message)s    (%(filename)s:%(lineno)d)"),
                              (30, "%(asctime)-22.19s \x1b[1m%(name)-21s\x1b[0m [\x1b[33m%(levelname)s\x1b[0m]:    %(message)s    (%(filename)s:%(lineno)d)"),
                              (40, "%(asctime)-22.19s \x1b[1m%(name)-21s\x1b[0m [\x1b[31m%(levelname)s\x1b[0m]:    %(message)s    (%(filename)s:%(lineno)d)"),
                              (50, "%(asctime)-22.19s \x1b[1m%(name)-21s\x1b[0m [\x1b[91m%(levelname)s\x1b[0m]:    %(message)s    (%(filename)s:%(lineno)d)")])
    def test_build_msg_format(self, levelno, expected_log_format):
        record = mock.MagicMock(spec=logging.LogRecord, levelno=levelno)
        log_fmt = ColorFormatter().build_msg_format(record)
        assert log_fmt == expected_log_format

    @pytest.mark.parametrize("status, expected_status",
                             [("100 Continue", '\x1b[97m100 Continue\x1b[0m'),
                              ("200 OK", '\x1b[32m200 OK\x1b[0m'),
                              ("300 Multiple Choices", '\x1b[33m300 Multiple Choices\x1b[0m'),
                              ("400 Bad Request", '\x1b[31m400 Bad Request\x1b[0m'),
                              ("500 Internal Server Error", '\x1b[91m500 Internal Server Error\x1b[0m'),
                              ("599 Unknown Error", "\x1b[91m599 Unknown Error\x1b[0m")])
    def test_format_request_msg(self, status, expected_status):
        expected_message = f'0.0.0.0:80 - "\x1b[1mGET /dummy/path HTTP/1.1\x1b[0m" {expected_status} - 0.32ms'
        result = ColorFormatter().format_request_msg(msg=request_msg_format,
                                                     host="0.0.0.0",
                                                     port=80,
                                                     method_path="GET /dummy/path HTTP/1.1",
                                                     status=status,
                                                     process_time=0.32)
        assert result == expected_message

    @pytest.mark.parametrize("level_no, level_name, color_fmt",
                             [(logging.NOTSET, "NOTSET", "34"),
                              (logging.DEBUG, "DEBUG", "36"),
                              (logging.INFO, "INFO", "32"),
                              (logging.WARNING, "WARNING", "33"),
                              (logging.ERROR, "ERROR", "31"),
                              (logging.CRITICAL, "CRITICAL", "91")])
    @mock.patch("{{cookiecutter.project_slug}}.app.utils.logging.logging.Formatter")
    def test_format(self, mocked_formatter, level_no, level_name, color_fmt):
        mocked_formatter.return_value.format.return_value = "dummy return"
        record = mock.MagicMock(spec=logging.LogRecord,
                                msg=request_msg_format,
                                args=("0.0.0.0",
                                      80,
                                      "GET /dummy/path HTTP/1.1",
                                      "200 OK",
                                      0.32),
                                levelno=level_no,
                                levelname=level_name,
                                name="dummy_logger")
        output = ColorFormatter().format(record)
        log_fmt = f'%(asctime)-22.19s \x1b[1m%(name)-21s\x1b[0m [\x1b[{color_fmt}' \
                  f'm%(levelname)s\x1b[0m]:    ' \
                  f'%(message)s    (%(filename)s:%(lineno)d)'
        mocked_formatter.assert_called_with(log_fmt)
        mocked_formatter.return_value.format.assert_called_with(record)
        assert output == "dummy return"