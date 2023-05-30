import pytest
import unittest.mock as mock
import click
from fastapi import Request, Response
from {{cookiecutter.project_slug}}.app.utils.logging import status_code_colors, get_request_msg_args


@pytest.mark.parametrize("key, color, expected_output",
                         [(1, "bright_white", "\x1b[97mhello\x1b[0m"),
                          (2, "green", "\x1b[32mhello\x1b[0m"),
                          (3, "yellow", "\x1b[33mhello\x1b[0m"),
                          (4, "red", "\x1b[31mhello\x1b[0m"),
                          (5, "bright_red", "\x1b[91mhello\x1b[0m")])
@mock.patch("{{cookiecutter.project_slug}}.app.utils.logging.click.style",
            side_effect=click.style)
def test_status_code_colours(mocked_click_style, key, color, expected_output):
    dummy_input = "hello"
    dummy_output = status_code_colors[key](dummy_input)
    mocked_click_style.assert_called_with(dummy_input, fg=color)
    assert dummy_output == expected_output


@pytest.mark.parametrize("response_status_code, expected_status",
                         [(100, '100 Continue'),
                          (200, '200 OK'),
                          (300, '300 Multiple Choices'),
                          (400, '400 Bad Request'),
                          (500, '500 Internal Server Error'),
                          (599, "599 Unknown Error")])
def test_get_request_msg_args(response_status_code, expected_status):
    expected_result_format = '0.0.0.0:80 - "\x1b[1mGET /dummy/path ' \
                             'HTTP/1.1\x1b[0m" {} - 0.32ms'
    request = mock.MagicMock(spec=Request,
                             method="GET",
                             url=mock.MagicMock(path="/dummy/path"),
                             scope=dict(http_version="1.1"),
                             client=mock.MagicMock(host="0.0.0.0", port=80))
    response = mock.MagicMock(spec=Response, status_code=response_status_code)
    host, port, method_path, status, process_time = get_request_msg_args(request, response, 0.32)
    assert host == "0.0.0.0"
    assert port == 80
    assert method_path == "GET /dummy/path HTTP/1.1"
    assert status == expected_status
    assert process_time == 0.32