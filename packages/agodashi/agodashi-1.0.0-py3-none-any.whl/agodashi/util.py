#!/usr/bin/env python3
# coding: utf-8
import itertools
import re
from typing import List, Set

import requests
from flask import abort
from werkzeug.datastructures import ImmutableMultiDict

from agodashi.cwl import (extract_cwl_wf_params, extract_cwl_wf_version,
                          get_cwltool_supported_languages, get_cwltool_version)
from agodashi.type import ServiceInfo, SupportedLanguage, WorkflowEngine


def generate_service_info() -> ServiceInfo:
    workflow_engines: List[WorkflowEngine] = []
    workflow_engines.append({
        "engine_name": "cwltool",
        "engine_version": get_cwltool_version(),
        "supported_languages": get_cwltool_supported_languages()
    })

    service_info: ServiceInfo = {
        "workflow_engines": workflow_engines,
        "supported_languages": generate_all_supported_languages()
    }

    return service_info


def generate_all_supported_languages() -> List[SupportedLanguage]:
    supported_languages: List[SupportedLanguage] = \
        [*get_cwltool_supported_languages()]
    unique_language_names: Set[str] = \
        {lang["language_name"] for lang in supported_languages}
    all_supported_languages: List[SupportedLanguage] = []
    for lang_name in unique_language_names:
        all_supported_languages.append({
            "language_name": lang_name,
            "language_versions": sorted(set(itertools.chain.from_iterable(
                [lang["language_versions"] for lang in supported_languages
                 if lang["language_name"] == lang_name]
            )))
        })

    return all_supported_languages


def validate_and_extract_request(
        form_data: ImmutableMultiDict,  # type: ignore
        form_files: ImmutableMultiDict) -> str:  # type: ignore

    require_keys: List[str] = ["wf_url", "wf_content", "wf_file"]
    data_keys: List[str] = list(form_data.keys())
    require_data_keys: List[str] = \
        [key for key in require_keys if key in data_keys]
    file_keys: List[str] = list(form_files.keys())
    require_file_keys: List[str] = \
        [key for key in require_keys if key in file_keys]
    keys: List[str] = require_data_keys + require_file_keys
    if len(keys) != 1:
        abort(400, "Please add one of wf_url, wf_content, or wf_file to the "
                   "request as form data.")
    key: str = keys[0]
    content: str
    if key == "wf_url":
        content = get_workflow_content_from_url(form_data[key])
    elif key == "wf_content":
        content = form_data[key]
    elif key == "wf_file":
        content = form_files[key].read().decode("utf-8")

    return content


def get_workflow_content_from_url(wf_url: str) -> str:
    try:
        res = requests.get(wf_url)
    except Exception:
        abort(400, f"The wf_url: {wf_url} you entered returned errors")
    if res.status_code != 200:
        abort(400, f"The wf_url: {wf_url} you entered returned a status "
                   f"code {res.status_code}")

    return res.text


def extract_wf_type(wf_content: str) -> str:
    wf_type: str
    for line in wf_content.splitlines():
        if re.search(r"(cwlVersion)", line):
            wf_type = "CWL"

    return wf_type


def extract_wf_version(wf_content: str, wf_type: str) -> str:
    if wf_type == "CWL":
        return extract_cwl_wf_version(wf_content)
    else:
        abort(400, "The requested workflow is not supported.")


def extract_wf_params(wf_content: str, wf_type: str) -> str:
    if wf_type == "CWL":
        return extract_cwl_wf_params(wf_content)
    else:
        abort(400, "The requested workflow is not supported.")
