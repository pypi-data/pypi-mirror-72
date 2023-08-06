"""component_loader
"""
import traceback
from typing import Any, Dict, List

from kubernetes.client.api_client import ApiClient

from dok8s.logger import LOGGER


def _fix_api_version(api_version: str = "") -> str:
    """_fix_api_version
    """
    if api_version == "NETWORKING.K8S.IO/V1BETA1":
        return "NetworkingV1beta1"
    api_version = (
        api_version.replace("APPS/", "")
        .replace("RBAC.AUTHORIZATION.K8S.IO/", "")
        .replace("POLICY/", "")
        .replace("BETA1", "beta1")
        .replace("APIREGISTRATION.K8S.IO/", "")
    )
    return api_version


def identify_kubernetes_object(data: Dict = None):
    """identify_kubernetes_object
    """
    if data is None:
        data = {}

    api_version: str = ""
    kind: str = ""
    klass: str = ""
    try:
        api_version = _fix_api_version(data["apiVersion"].upper())
        kind = data["kind"]
        klass = api_version + kind
    except KeyError as error:
        track = traceback.format_exc()
        LOGGER.error(error)
        LOGGER.debug(track)

    if not klass:
        return None

    try:
        client = ApiClient()
        obj = client._ApiClient__deserialize(data, klass)
        return obj
    except AttributeError as error:
        track = traceback.format_exc()
        LOGGER.error(error)
        LOGGER.debug(track)


def generate_component_output(obj: Any = None) -> List:
    """generate_component_output
    """

    def config_map():
        kind = obj.kind
        name = obj.metadata.name
        filenames = "--"
        if obj.data:
            filenames = ", ".join(obj.data)
        return [kind, name, filenames]

    def deployment():
        kind = obj.kind
        name = obj.metadata.name
        init_containers = obj.spec.template.spec.init_containers
        containers = obj.spec.template.spec.containers
        if init_containers:
            containers = containers + init_containers
        containers = ", ".join([x.name for x in containers])
        return [kind, name, containers]

    def ingress():
        kind = obj.kind
        hosts = ", ".join([x.host for x in obj.spec.rules])
        notes = "Customisable"
        return [kind, hosts, notes]

    def persistent_volume_claim():
        kind = obj.kind
        name = obj.metadata.name
        size = obj.spec.resources.requests["storage"]
        return [kind, name, size]

    def secret():
        kind = obj.kind
        name = obj.metadata.name
        return [kind, name, "--"]

    def service():
        kind = obj.kind
        name = obj.metadata.name
        ports = ", ".join([str(x.port) for x in obj.spec.ports])
        return [kind, name, ports]

    def stateful_set():
        kind = obj.kind
        name = obj.metadata.name
        init_containers = obj.spec.template.spec.init_containers
        containers = obj.spec.template.spec.containers
        if init_containers:
            containers = containers + init_containers
        containers = [x.name for x in containers]
        volumes = obj.spec.volume_claim_templates
        volumes = [
            f'{x.metadata.name} ({x.spec.resources.requests["storage"]})'
            for x in volumes
        ]
        notes = ", ".join(containers + volumes)
        return [kind, name, notes]

    def default():
        kind = obj.kind
        name = obj.metadata.name
        return [kind, name, "--"]

    switcher = {
        "ConfigMap": config_map,
        "Deployment": deployment,
        "Ingress": ingress,
        "PersistentVolumeClaim": persistent_volume_claim,
        "Secret": secret,
        "Service": service,
        "StatefulSet": stateful_set,
    }

    def switch(kind):
        return switcher.get(kind, default)()

    return switch(obj.kind)


def generate_docker_output(obj: Any = None):
    """generate_docker_output
    """

    def details():
        service = obj.metadata.name
        init_containers = obj.spec.template.spec.init_containers
        containers = obj.spec.template.spec.containers
        if init_containers:
            containers = containers + init_containers
        name = []
        image = []
        version = []
        for container in containers:
            image_details = container.image.split(":")
            name.append(container.name)
            image.append(image_details[0])
            version.append(image_details[1])
        names = ", ".join(name)
        images = ", ".join(image)
        versions = ", ".join(version)
        return [service, names, images, versions]

    def default():
        return []

    switcher = {
        "Deployment": details,
        "StatefulSet": details,
    }

    def switch(kind):
        return switcher.get(kind, default)()

    return switch(obj.kind)


def generate_resource_output(obj: Any = None) -> List:
    """generate_resource_output
    """

    def details():
        service = obj.metadata.name
        init_containers = obj.spec.template.spec.init_containers
        containers = obj.spec.template.spec.containers
        if init_containers:
            containers = containers + init_containers
        name = []
        request = []
        limit_request = []
        for container in containers:
            name.append(container.name)
            if container.resources:
                if container.resources.requests:
                    cpu = container.resources.requests.get("cpu", "--")
                    ram = container.resources.requests.get("memory", "--")
                    request.append(f"CPU:{cpu} Memory:{ram}")
                if container.resources.limits:
                    cpu_limit = container.resources.limits.get("cpu", "--")
                    ram_limit = container.resources.limits.get("memory", "--")
                    limit_request.append(f"CPU:{cpu_limit} Memory:{ram_limit}")
            else:
                request.append("N/A")
                limit_request.append("N/A")
        names = ", ".join(name)
        requests = ", ".join(request)
        limit_requests = ", ".join(limit_request)
        return [service, names, requests, limit_requests, "--"]

    def default():
        return []

    switcher = {
        "Deployment": details,
        "StatefulSet": details,
    }

    def switch(kind):
        return switcher.get(kind, default)()

    return switch(obj.kind)
