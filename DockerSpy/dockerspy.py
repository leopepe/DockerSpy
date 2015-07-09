__author__ = 'leonardo'

__author__ = 'leonardo'

from docker import Client


class DockerSpy:
    """

    """
    def __init__(self, container=None, container_api_url='unix://var/run/docker.sock'):
        """
        :rtype: object
        :type DockerSpy: object
        """
        self._client = Client(base_url=container_api_url)
        self.containers = {}
        if container:
            self.containers[container] = self._client.inspect_container(container=container)

        self.tagged_containers = {}

    def get_containers(self):
        """
        :rtype : list
        :return: containers
        """
        try:
            # list live containers names using list comprehension
            containers = [container['Names'][0].replace('/', '') for container in self._client.containers()]
            return containers
        except Exception:
            raise

    @staticmethod
    def _into_dict(kv_config):
        env_dict = {}
        for item in kv_config:
            k, v = item.split('=', 1)
            env_dict[k] = v
        return env_dict

    @property
    def describe_containers(self):
        # update self.containers
        for name in self.get_containers():
            self.containers[name] = self._client.inspect_container(name)
            self.containers[name]['Config']['Env'] = self._into_dict(kv_config=self.containers[name]['Config']['Env'])

        return self.containers

    def events(self):
        """

        """
        try:
            return self._client.events(decode=True)
        except KeyboardInterrupt:
            pass

    def env(self, container=None):
        """

        :rtype: dict
        :return: container's environment variable
        """
        """
        # internal method to transform k=v environment variable into dict
        def _into_dict(kv_config):
            env_dict = {}
            for item in kv_config:
                k, v = item.split('=', 1)
                env_dict[k] = v
            return env_dict
        """
        # If self.cotnainers exists or grater then 0 return Config.Env
        if self.containers:
            return self.containers[container]['Config']['Env']
        else:
            return self.describe_containers[container]['Config']['Env']

    def virtual_port(self, container):
        # internal method to transform k=v environment variable into dict
        """
        def _into_dict(kv_config):
            env_dict = {}
            for item in kv_config:
                k, v = item.split('=', 1)
                env_dict[k] = v
            return env_dict
        """
        # return config env of a container in dictionary format
        if self.containers:
            return self.env(container)['VIRTUAL_PORT']
        else:
            return self.describe_containers[container]['Config']['Env']['VIRTUAL_PORT']

    def ip_address(self, container):
        if self.containers:
            return self.containers[container]['NetworkSettings']['IPAddress']
        else:
            return self.describe_containers[container]['NetworkSettings']['IPAddress']

    def memberof(self, service_name):
        pass


if __name__ == '__main__':
    docker = DockerSpy()
    # print(docker.describe_containers)
    # print(docker.env(container='chargeback-sync'))
    # print(docker.virtual_port(container='chargeback-sync'))
    # print(docker.ip_address(container='chargeback-sync'))
    # docker.events()
    # for container, info in docker.describe_containers.items():
    #     print(getattr(docker, 'containers')['chargeback-sync'])

