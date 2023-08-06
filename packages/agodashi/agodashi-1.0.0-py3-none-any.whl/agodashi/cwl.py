#!/usr/bin/env python3
# coding: utf-8
import json
import os
import subprocess
from tempfile import mkstemp
from typing import Any, List, cast

import yaml
from cwltool.update import ALLUPDATES
from cwltool.utils import versionstring
from flask import abort

from agodashi.type import SupportedLanguage


def get_cwltool_version() -> str:
    version: str = cast(str, versionstring().split(" ")[1])
    return version


def get_cwltool_supported_languages() -> List[SupportedLanguage]:
    return [{
        "language_name": "CWL",
        "language_versions": sorted(ALLUPDATES)
    }]


def extract_cwl_wf_version(wf_content: str) -> str:
    wf_obj: Any
    try:
        wf_obj = yaml.safe_load(wf_content)
    except Exception:
        pass
    try:
        wf_obj = json.loads(wf_content)
    except Exception:
        pass
    if wf_obj is None:
        abort(400, "The requested CWL workflow is neither json nor yaml.")
    if "cwlVersion" not in wf_obj:
        abort(400,
              "The requested CWL workflow does not contain cwlVersion field.")

    return wf_obj["cwlVersion"]  # type: ignore


def extract_cwl_wf_params(wf_content: str) -> str:
    _, wf_file = mkstemp(text=True)
    with open(wf_file, mode="w") as f:
        f.write(wf_content)
        f.flush()
    process = subprocess.run(
        ["cwltool", "--make-template", wf_file],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        encoding="utf-8",
    )
    os.remove(wf_file)
    if process.returncode != 0:
        abort(400,
              f"cwltool ended with status {process.returncode}\n"
              f"The stderr of cwltool is as follows:\n"
              f"{process.stderr}"
              )

    return process.stdout
