# Agodashi

[![pytest](https://github.com/suecharo/agodashi/workflows/pytest/badge.svg)](https://github.com/suecharo/agodashi/actions?query=workflow%3Apytest)
[![flake8](https://github.com/suecharo/agodashi/workflows/flake8/badge.svg)](https://github.com/suecharo/agodashi/actions?query=workflow%3Aflake8)
[![isort](https://github.com/suecharo/agodashi/workflows/isort/badge.svg)](https://github.com/suecharo/agodashi/actions?query=workflow%3Aisort)
[![mypy](https://github.com/suecharo/agodashi/workflows/mypy/badge.svg)](https://github.com/suecharo/agodashi/actions?query=workflow%3Amypy)
[![Apache License](https://img.shields.io/badge/license-Apache%202.0-orange.svg?style=flat&color=important)](http://www.apache.org/licenses/LICENSE-2.0)

Agodashi is a simple REST API server.
It takes a workflow file written in workflow language as input and returns workflow type, workflow version and workflow parameters template.
Currently, supported workflow languages are as follows:

- [Common Workflow Language (CWL)](https://www.commonwl.org)

In the future, we plan to support the following languages.

- [Nextflow](https://www.nextflow.io)
- [Snakemake](https://snakemake.readthedocs.io/en/stable/)
- [Workflow Description Language (WDL)](https://openwdl.org)


## Install and Run

Agodashi supports Python 3.6 or newer.

```bash
$ pip3 install agodashi
$ agodashi
```

### Docker

We also expect to launch using Docker.

```bash
# Launch
$ docker-compose up -d

# Launch confirmation
$ docker-compose logs
```

## Usage

As API specifications, please check [SwaggerUI - Agodashi API Spec](https://suecharo.github.io/agodashi-swagger-ui/)

The help for the Agodashi startup command is as follows.

```bash
$ agodashi --help
usage: agodashi [-h] [--host] [-p] [--debug]

An API server for parsing workflows written in workflow languages

optional arguments:
  -h, --help    show this help message and exit
  --host        Host address of Flask. (default: 127.0.0.1)
  -p , --port   Port of Flask. (default: 8080)
  --debug       Enable debug mode of Flask.
```

As the simplest example of a REST API Request, here is the result of a `GET /inspect-workflow`.

```json
GET /inspect-workflow -F 'wf_url=https://raw.githubusercontent.com/suecharo/agodashi/master/tests/resources/cwl/trimming_and_qc_packed.cwl'

{
  "wf_params": "nthreads: 2  # default value of type \"int\". (optional)\nfastq_2:  # type \"File\"\n    class: File\n    path: a/file/path\nfastq_1:  # type \"File\"\n    class: File\n    path: a/file/path\n",
  "wf_type": "CWL",
  "wf_version": "v1.0"
}
```

## Development

You can start the development environment as follows.

```bash
$ docker-compose -f docker-compose.dev.yml up -d --build
$ docker-compose -f docker-compose.dev.yml exec app bash
```

We use [flake8](https://pypi.org/project/flake8/), [isort](https://github.com/timothycrosley/isort), and [mypy](http://mypy-lang.org) as the Linter.

```bash
$ bash ./tests/lint_and_style_check/flake8.sh
$ bash ./tests/lint_and_style_check/isort.sh
$ bash ./tests/lint_and_style_check/mypy.sh
```

We use [pytest](https://docs.pytest.org/en/latest/) as a Test Tool.

```bash
$ pytest .
```

## License

[Apache-2.0](https://www.apache.org/licenses/LICENSE-2.0). See the [LICENSE](https://github.com/suecharo/agodashi/blob/master/LICENSE).
