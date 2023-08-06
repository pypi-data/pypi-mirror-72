[![github latest release](https://badgen.net/github/release/nichelia/dok8s?icon=github)](https://github.com/nichelia/dok8s/releases/latest/)
[![pypi latest package](https://badgen.net/pypi/v/dok8s?label=pypi%20pacakge)](https://pypi.org/project/dok8s/)
[![docker latest image](https://img.shields.io/docker/v/nichelia/dok8s?label=image&logo=docker&logoColor=white)](https://hub.docker.com/repository/docker/nichelia/dok8s)
[![project license](https://badgen.net/github/license/nichelia/dok8s?color=purple)](https://github.com/nichelia/dok8s/blob/master/LICENSE)

![dok8s CI](https://github.com/nichelia/dok8s/workflows/dok8s%20CI/badge.svg)
![dok8s CD](https://github.com/nichelia/dok8s/workflows/dok8s%20CD/badge.svg)
[![security scan](https://badgen.net/dependabot/nichelia/dok8s/?label=security%20scan)](https://github.com/nichelia/dok8s/labels/security%20patch)
[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen)](https://github.com/pre-commit/pre-commit)


[![code coverage](https://badgen.net/codecov/c/github/nichelia/dok8s?label=code%20coverage)](https://codecov.io/gh/nichelia/dok8s)
[![code alerts](https://badgen.net/lgtm/alerts/g/nichelia/dok8s?label=code%20alerts)](https://lgtm.com/projects/g/nichelia/dok8s/alerts/)
[![code quality](https://badgen.net/lgtm/grade/g/nichelia/dok8s?label=code%20quality)](https://lgtm.com/projects/g/nichelia/dok8s/context:python)
[![code style](https://badgen.net/badge/code%20style/black/color=black)](https://github.com/ambv/black)

# dok8s
dok8s: Output notes for a Kubernetes deployment.


## Contents
1. [Use Case](#use-case)
2. [Configuration](#configuration)
3. [Development](#development)
4. [Testing](#testing)
5. [Versioning](#versioning)
6. [Deployment](#deployment)
7. [Production](#production)

## Use Case

Collect and export information about a Kubernetes deployment (such as components, resources and docker images/tags) in a table format.
Input: Deployment files (collection of YAML definitions).  
Output: Pretty-print tabular data.

### Requirements

* Parse the following Kubernetes components:  
  `ConfigMap`, `Deployment`, `Ingress`, `PersistentVolumeClaim`, `Secret`, `Service`, `StatefulSet`.
* Collect relevant information:  
  `kind`, `metadata name`, `data filenames`, `(init) containers`, `hosts / rules`, `storage name / size`, `ports`, `cpu/memory requests/limits`
* Production-ready code.

### Assumptions

* Parsed Kubernetes components are included in the [official python Kubernetes client](https://github.com/kubernetes-client/python)

### Design

This project is based on a CLI interface.

### Example Output

#### Input
YAML file: [Cluster Autoscaler](https://raw.githubusercontent.com/kubernetes/autoscaler/master/cluster-autoscaler/cloudprovider/aws/examples/cluster-autoscaler-autodiscover.yaml)

#### Output

Components

| Component          | Value              | Details            |
|:-------------------|:-------------------|:-------------------|
| ClusterRole        | cluster-autoscaler | --                 |
| ClusterRoleBinding | cluster-autoscaler | --                 |
| Deployment         | cluster-autoscaler | cluster-autoscaler |
| Role               | cluster-autoscaler | --                 |
| RoleBinding        | cluster-autoscaler | --                 |
| ServiceAccount     | cluster-autoscaler | --                 |

Resources

| Platform/Service   | Name               | Request               | Limit Request         | Notes   |
|:-------------------|:-------------------|:----------------------|:----------------------|:--------|
| cluster-autoscaler | cluster-autoscaler | CPU:100m Memory:300Mi | CPU:100m Memory:300Mi | --      |

Docker images

| Platform/Service   | Name               | Image                         | Version   |
|:-------------------|:-------------------|:------------------------------|:----------|
| cluster-autoscaler | cluster-autoscaler | k8s.gcr.io/cluster-autoscaler | v1.14.7   |


## Configuration

Behaviour of the application can be configured via Environment Variables.

| Environment Variable | Description | Type | Default Value |
| -------------- | -------------- | -------------- | -------------- |
| `DOK8S_LOG_LEVEL` | Level of logging - overrides verbose/quiet flag | string | - |
| `DOK8S_LOG_DIR` | Directory to save logs | string | - |
| `DOK8S_BIN_DIR` | Directory to save any output (bin) | string | bin |

## Development

### Configure your local development

* Clone [repo](https://github.com/nichelia/dok8s) on your local machine
* Install [`conda`](https://www.anaconda.com) or [`miniconda`](https://docs.conda.io/en/latest/miniconda.html)
* Create your local project environment (based on [`conda`](https://www.anaconda.com), [`poetry`](https://python-poetry.org), [`pre-commit`](https://pre-commit.com)):  
`$ make env`
* (Optional) Update existing local project environment:  
`$ make env-update`

### Run locally

On a terminal, run the following (execute on project's root directory):

* Activate project environment:  
`$ . ./scripts/helpers/environment.sh`
* Run the CLI using `poetry`:  
`$ dok8s`

### Contribute

[ Not Available ]

## Testing
(part of CI/CD)

[ Work in progress... ]

To run the tests, open a terminal and run the following (execute on project's root directory):

* Activate project environment:  
`$ . ./scripts/helpers/environment.sh`
* To run pytest:  
`$ make test`
* To check test coverage:  
`$ make test-coverage`

## Versioning

Increment the version number:  
`$ poetry version {bump rule}`  
where valid bump rules are:

1. patch
2. minor
3. major
4. prepatch
5. preminor
6. premajor
7. prerelease

### Changelog

Use `CHANGELOG.md` to track the evolution of this package.  
The `[UNRELEASED]` tag at the top of the file should always be there to log the work until a release occurs.  

Work should be logged under one of the following subtitles:
* Added
* Changed
* Fixed
* Removed

On a release, a version of the following format should be added to all the current unreleased changes in the file.  
`## [major.minor.patch] - YYYY-MM-DD`

## Deployment

### Pip package

On a terminal, run the following (execute on project's root directory):

* Activate project environment:  
`$ . ./scripts/helpers/environment.sh`
* To build pip package:  
`$ make build-package`
* To publish pip package (requires credentials to PyPi):  
`$ make publish-package`

### Docker image

On a terminal, run the following (execute on project's root directory):

* Activate project environment:  
`$ . ./scripts/helpers/environment.sh`
* To build docker image:  
`$ make build-docker`

## Production

For production, a Docker image is used.
This image is published publicly on [docker hub](https://hub.docker.com/repository/docker/nichelia/dok8s).

* First pull image from docker hub:  
`$ docker pull nichelia/dok8s:{version}`
* Execute CLI via docker run:  
`$ docker run --rm -it -v ~/dok8s_bin:/tmp/bin nichelia/dok8s:{version} {command} -d /tmp/bin -o {filename}`  
This command mounts the application's bin (outcome) to user's root directory under dok8s_bin folder. The Kubernetes YAML files you want to parse, should be included in this directory.

where version is the published application version
