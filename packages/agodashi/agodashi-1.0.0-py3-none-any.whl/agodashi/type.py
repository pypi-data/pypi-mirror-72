#!/usr/bin/env python3
# coding: utf-8
from sys import version_info
from typing import List

if version_info.minor < 8:
    from typing_extensions import TypedDict
else:
    from typing import TypedDict  # type: ignore


class SupportedLanguage(TypedDict):
    language_name: str
    language_versions: List[str]


class WorkflowEngine(TypedDict):
    engine_name: str
    engine_version: str
    supported_languages: List[SupportedLanguage]


class ServiceInfo(TypedDict):
    workflow_engines: List[WorkflowEngine]
    supported_languages: List[SupportedLanguage]


class AllInformation(TypedDict):
    wf_type: str
    wf_version: str
    wf_params: str


class Type(TypedDict):
    wf_type: str


class Version(TypedDict):
    wf_version: str


class Parameters(TypedDict):
    wf_params: str


class ErrorResponse(TypedDict):
    """
    An object that can optionally include information about the error.
    msg:
        A detailed error message.
    status_code:
        The integer representing the HTTP status code (e.g. 200, 404).
    """
    msg: str
    status_code: int
