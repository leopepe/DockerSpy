#!/bin/env python
__author__ = 'leonardo'

from dockerspy import DockerSpy
from parser import TemplateParser
from subprocess import call
import os
import sys

# constants
PROJECT_DIR = os.path.abspath(os.path.dirname(__file__))
TEMPLATE_DIR = os.path.join(PROJECT_DIR, 'templates')
TEMPLATE_DEFAULT = os.path.join(TEMPLATE_DIR, 'default.conf')
TEMPLATE = os.path.join(TEMPLATE_DIR, 'node.nodomain.conf')
NGINX_CONFIG = os.path.abspath('/etc/nginx/conf.d')


def main():
    docker = DockerSpy(container_api_url='unix://var/run/docker.sock')
    parser = TemplateParser(template_path=TEMPLATE)

    def _config_gen():
        for container in docker.describe_containers:
            node_config_file = '/etc/nginx/conf.d/{0}.conf'.format(container)
            if docker.containers[container]['Config']['Env']['VIRTUAL_HOST'] and docker.containers[container]['Config']['Env']['VIRTUAL_PORT']:
                data = parser.replace_data(ip=docker.containers[container]['NetworkSettings']['IPAddress'],
                                           vhost=docker.containers[container]['Config']['Env']['VIRTUAL_HOST'],
                                           port=docker.containers[container]['Config']['Env']['VIRTUAL_PORT'])
                with open(node_config_file, 'w+') as config_file:
                    config_file.write(data)

        call(['/etc/init.d/nginx', 'reload'])

    sys.stdout.write('DockerSpy: Generating nodes config files')
    _config_gen()

    while True:
        for event in docker.events().__iter__():
            if event['status'] == 'start':
                sys.stdout.write('DockerSpy: Generating nodes config files from started containers')
                _config_gen()
            elif event['status'] == 'stop':
                sys.stdout.write('DockerSpy: Generating nodes config files from stopped containers')
                container_name = event['from'].split('/')[1] + '.conf'
                node = os.path.join(NGINX_CONFIG, container_name)
                os.remove(node)
                call(['/etc/init.d/nginx', 'reload'])

if __name__ == '__main__':
    main()
