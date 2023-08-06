#!/usr/bin/env python3
# coding: utf-8
import os
import sys
from argparse import ArgumentParser, Namespace
from traceback import format_exc
from typing import Dict, List, Optional, Union

from flask import Flask, Response, current_app, jsonify
from werkzeug.exceptions import HTTPException

from agodashi.const import DEFAULT_CROS, DEFAULT_HOST, DEFAULT_PORT
from agodashi.controller import app_bp
from agodashi.type import ErrorResponse


def parse_args(sys_args: List[str]) -> Namespace:
    parser: ArgumentParser = ArgumentParser(
        description="An API server for parsing workflows written in " +
                    "workflow languages")

    parser.add_argument(
        "--host",
        nargs=1,
        type=str,
        metavar="",
        help=f"Host address of Flask. (default: {DEFAULT_HOST})"
    )
    parser.add_argument(
        "-p",
        "--port",
        nargs=1,
        type=int,
        metavar="",
        help=f"Port of Flask. (default: {DEFAULT_PORT})"
    )
    parser.add_argument(
        "--debug",
        action="store_true",
        help="Enable debug mode of Flask."
    )

    args: Namespace = parser.parse_args(sys_args)

    return args


def handle_default_params(args: Namespace) -> Dict[str, Union[str, int]]:
    params: Dict[str, Union[str, int]] = {
        "host": handle_default_host(args.host),
        "port": handle_default_port(args.port),
        "debug": handle_default_debug(args.debug),
    }

    return params


def handle_default_host(host: Optional[List[str]]) -> str:
    if host is None:
        return os.environ.get("AGODASHI_HOST", DEFAULT_HOST)

    return host[0]


def handle_default_port(port: Optional[List[str]]) -> int:
    if port is None:
        return int(os.environ.get("AGODASHI_PORT", DEFAULT_PORT))

    return int(port[0])


def handle_default_debug(debug: bool) -> bool:
    if debug is False:
        return str2bool(os.environ.get("AGODASHI_DEBUG", False))

    return debug


def str2bool(val: Union[str, bool]) -> bool:
    if isinstance(val, bool):
        return val
    return False if val.lower() in ["false", "no", "n"] else bool(val)


def fix_errorhandler(app: Flask) -> Flask:
    @app.errorhandler(400)
    @app.errorhandler(401)
    @app.errorhandler(403)
    @app.errorhandler(404)
    @app.errorhandler(500)
    def error_handler(error: HTTPException) -> Response:
        res_body: ErrorResponse = {
            "msg": error.description,  # type: ignore
            "status_code": error.code,  # type: ignore
        }
        response: Response = jsonify(res_body)
        response.status_code = error.code  # type: ignore
        return response

    @app.errorhandler(Exception)
    def error_handler_exception(exception: Exception) -> Response:
        current_app.logger.error(exception.args[0])
        current_app.logger.debug(format_exc())
        res_body: ErrorResponse = {
            "msg": "The server encountered an internal error and was " +
                   "unable to complete your request.",
            "status_code": 500,
        }
        if current_app.config["TESTING"]:
            res_body["msg"] = format_exc()
        response: Response = jsonify(res_body)
        response.status_code = 500
        return response

    return app


def add_headers(app: Flask) -> Flask:
    @app.after_request
    def after_request_func(response: Response) -> Response:
        response.headers["Access-Control-Allow-Origin"] = \
            os.environ.get("AGODASHI_CROS", DEFAULT_CROS)

        return response

    return app


def create_app(params: Dict[str, Union[str, int]]) -> Flask:
    app = Flask(__name__)
    app.register_blueprint(app_bp)
    fix_errorhandler(app)
    add_headers(app)

    return app


def main() -> None:
    args: Namespace = parse_args(sys.argv[1:])
    params: Dict[str, Union[str, int]] = handle_default_params(args)
    app: Flask = create_app(params)
    app.run(host=params["host"],  # type: ignore
            port=params["port"],  # type: ignore
            debug=params["debug"])  # type: ignore


if __name__ == "__main__":
    main()
