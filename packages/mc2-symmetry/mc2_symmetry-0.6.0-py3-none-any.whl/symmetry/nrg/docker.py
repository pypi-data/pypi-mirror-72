import docker

from symmetry.api import ServiceDescription


class DockerGateway:
    docker_port = '2376'

    def __init__(self, docker_port=None) -> None:
        super().__init__()
        self.docker_port = docker_port or DockerGateway.docker_port

    def start_service_container(self, node_ip, service: ServiceDescription, port):
        client = docker.DockerClient(base_url='tcp://' + node_ip + ':' + self.docker_port)

        if service.image_file:
            images = client.images.load(service.image_file)
            if service.image not in images[0].tags:
                raise ValueError(f'given tag ({service.image}) must be provided by uploaded image')

        ports = {
            service.port: port
        }

        client.containers.run(service.image, command=service.command, detach=True, name=service.id, ports=ports)
        client.close()

    def list_containers(self, node_ip):
        client = docker.DockerClient(base_url='tcp://' + node_ip + ':' + self.docker_port, timeout=2)
        try:
            return client.containers.list(all=True)
        finally:
            client.close()

    def remove_service_container(self, node_ip, service_id):
        client = docker.DockerClient(base_url='tcp://' + node_ip + ':' + self.docker_port, timeout=2)
        container = client.containers.get(service_id)
        container.remove(force=True)
        client.close()