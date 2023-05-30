"""Define logging related utility functions and classes."""
import logging
import click
from http import HTTPStatus
from fastapi import Request, Response

status_code_colors = {
    1: lambda code: click.style(str(code), fg="bright_white"),
    2: lambda code: click.style(str(code), fg="green"),
    3: lambda code: click.style(str(code), fg="yellow"),
    4: lambda code: click.style(str(code), fg="red"),
    5: lambda code: click.style(str(code), fg="bright_red"),
}
request_msg_format = "%s:%d - \"%s\" %s - %.2fms"


def get_request_msg_args(request: Request, response: Response,
                         process_time: float) -> tuple:
    """Format the message for processing a http request.

    Args:
        request (Request): http request.
        response (Response): the corresponding response to the request.
        process_time (float): process time for the http request.

    Returns:
        tuple: the requisite args to format the message
    """
    try:
        response_status = HTTPStatus(response.status_code)
        status = f"{response_status.value} {response_status.phrase}"
    except ValueError:
        status = f"{response.status_code} Unknown Error"
    method_path = f"{request.method} {request.url.path} HTTP/{request.scope['http_version']}"
    args = (request.client.host, request.client.port,  # type: ignore
            method_path, status, process_time)
    return args


class StandardFormatter(logging.Formatter):
    """Logging Formatter to count warning / errors"""
    msg_format = "%(asctime)-22.19s %(name)-21s [%(levelname)s]:    " \
                 "%(message)s    (%(filename)s:%(lineno)d)"

    def build_msg_format(self, *args, **kwargs) -> str:
        """Wrapper function for building message customized format.

        Returns:
            str: log message format.
        """
        return self.msg_format

    def format(self, record: logging.LogRecord) -> str:
        """Format the given record to a log message.

        Args:
            record (logging.LogRecord): log record to format a log message.

        Returns:
            str: formatted log message.
        """
        log_fmt = self.build_msg_format(record)
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)


class ColorFormatter(StandardFormatter):
    """Logging Formatter to add colors and count warning / errors"""
    msg_format = "%(asctime)-22.19s {bold_name} {color_levelname:29}" \
                 "%(message)s    (%(filename)s:%(lineno)d)"

    level_name_colors = {
        logging.DEBUG: lambda level_name: click.style(str(level_name),
                                                      fg="cyan"),
        logging.INFO: lambda level_name: click.style(str(level_name),
                                                     fg="green"),
        logging.WARNING: lambda level_name: click.style(str(level_name),
                                                        fg="yellow"),
        logging.ERROR: lambda level_name: click.style(str(level_name),
                                                      fg="red"),
        logging.CRITICAL: lambda level_name: click.style((level_name),
                                                         fg="bright_red"),
        logging.NOTSET: lambda level_name: click.style(str(level_name),
                                                       fg="blue")
    }

    @staticmethod
    def format_request_msg(msg: str, host: str, port: int,
                           method_path: str, status: str,
                           process_time: float) -> str:
        """Format the message for processing a http request.

        Args:
            msg (str): http request.
            host (str): host of the running service
            port (int): listening port of the running service
            method_path (str): method path information of the request.
            status (str): status information including status code and statue phrase.
            process_time (float): process time for the http request.

        Returns:
            str: the formatted message, containing process time and http request and
            response related information
        """
        method_path = click.style(method_path, bold=True)
        status_code = int(status.split(" ")[0])
        status_func = status_code_colors[status_code // 100]
        status = status_func(status)
        return msg % (host, port, method_path, status, process_time)

    def build_msg_format(self, record: logging.LogRecord) -> str:  # type: ignore
        """Rendering message with colored format.

        Args:
            record (logging.LogRecord): log record to format a log message.

        Returns:
            str: log message format.
        """
        color_func = self.level_name_colors.get(record.levelno, lambda x: x)
        log_fmt = self.msg_format.format(
            color_levelname="[" + color_func("%(levelname)s") + "]:",
            bold_name=click.style("%(name)-21s", bold=True))
        return log_fmt

    def format(self, record: logging.LogRecord) -> str:
        """Format the given record to a log message.

        Args:
            record (logging.LogRecord): log record to format a log message.

        Returns:
            str: formatted log message.
        """
        if record.msg == request_msg_format:
            message = self.format_request_msg(record.msg, *record.args)  # type: ignore
            record.msg = message
            record.args = ()
        return super(ColorFormatter, self).format(record)
