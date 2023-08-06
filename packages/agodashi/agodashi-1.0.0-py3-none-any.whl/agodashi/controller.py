#!/usr/bin/env python3
# coding: utf-8
from flask import Blueprint, Response, jsonify, request

from agodashi.const import GET_STATUS_CODE
from agodashi.type import (AllInformation, Parameters, ServiceInfo, Type,
                           Version)
from agodashi.util import (extract_wf_params, extract_wf_type,
                           extract_wf_version, generate_service_info,
                           validate_and_extract_request)

app_bp = Blueprint("agodashi", __name__)


@app_bp.route("/service-info", methods=["GET"])
def get_service_info() -> Response:
    """
    Response to the name and version of workflow engines to be used inside the
    API Service. Also, it may be possible to extract the type, version and
    parameters of a workflow without using workflow engines. Therefore,
    workflow types and versions supported by this service are also responded
    to. The logic for determining workflow type and version is completely
    implementation-dependent.
    """
    res_body: ServiceInfo = generate_service_info()
    response: Response = jsonify(res_body)
    response.status_code = GET_STATUS_CODE

    return response


@app_bp.route("/inspect-workflow", methods=["GET"])
def inspect_workflow() -> Response:
    """
    This endpoint is used to inspect workflow. The parameter should be
    used one of wf_url, wf_content or wf_file.
    """
    wf_content: str = validate_and_extract_request(
        request.form, request.files)  # type: ignore
    wf_type: str = extract_wf_type(wf_content)
    res_body: AllInformation = {
        "wf_type": wf_type,
        "wf_version": extract_wf_version(wf_content, wf_type),
        "wf_params": extract_wf_params(wf_content, wf_type)
    }
    response: Response = jsonify(res_body)
    response.status_code = GET_STATUS_CODE

    return response


@app_bp.route("/inspect-workflow/type", methods=["GET"])
def inspect_workflow_type() -> Response:
    """
    This endpoint is used to inspect workflow type. The parameter should be
    used one of wf_url, wf_content or wf_file.
    """
    wf_content: str = validate_and_extract_request(
        request.form, request.files)  # type: ignore
    wf_type: str = extract_wf_type(wf_content)
    res_body: Type = {
        "wf_type": wf_type
    }
    response: Response = jsonify(res_body)
    response.status_code = GET_STATUS_CODE

    return response


@app_bp.route("/inspect-workflow/version", methods=["GET"])
def inspect_workflow_version() -> Response:
    """
    This endpoint is used to inspect workflow version. The parameter should be
    used one of wf_url, wf_content or wf_file.
    """
    wf_content: str = validate_and_extract_request(
        request.form, request.files)  # type: ignore
    wf_type: str = extract_wf_type(wf_content)
    res_body: Version = {
        "wf_version": extract_wf_version(wf_content, wf_type)
    }
    response: Response = jsonify(res_body)
    response.status_code = GET_STATUS_CODE

    return response


@app_bp.route("/inspect-workflow/parameters", methods=["GET"])
def inspect_workflow_parameters() -> Response:
    """
    This endpoint is used to inspect workflow parameters. The parameter should
    be used one of wf_url, wf_content or wf_file.
    """
    wf_content: str = validate_and_extract_request(
        request.form, request.files)  # type: ignore
    wf_type: str = extract_wf_type(wf_content)
    res_body: Parameters = {
        "wf_params": extract_wf_params(wf_content, wf_type)
    }
    response: Response = jsonify(res_body)
    response.status_code = GET_STATUS_CODE

    return response
