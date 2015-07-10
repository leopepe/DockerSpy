#!/usr/bin/env python
__author__ = 'leonardo'

from subprocess import call
import os
import sys
from DockerSpy.dockerspy import DockerSpy
from DockerSpy.parsers import TemplateParser
from DockerSpy import config

"""
# constants
PROJECT_DIR = os.path.abspath(os.path.dirname(__file__))
TEMPLATE_DIR = os.path.join(PROJECT_DIR, 'templates')
TEMPLATE = os.path.join(TEMPLATE_DIR, 'node.nodomain.conf')
NGINX_CONFIG = os.path.abspath('/etc/nginx/conf.d')
"""

def main():
    options = config.configurator().parse_args()
    template = options.template_path
    nginx_conf_dir = options.output_dir
    api_url = options.api_url
    docker = DockerSpy(container_api_url=api_url)
    parser = TemplateParser(template_path=template)

    def _config_gen():
        """

        :rtype : object
        """
        for container in docker.describe_containers:
            # local vars to easy code management
            vhost = docker.containers[container]['Config']['Env']['VIRTUAL_HOST']
            port = docker.containers[container]['Config']['Env']['VIRTUAL_PORT']
            ip = docker.containers[container]['NetworkSettings']['IPAddress']
            # node name created based on containers name
            node_config_file = '/etc/nginx/conf.d/{0}.conf'.format(container)
            if vhost and port:
                data = parser.replace_data(ip=ip, vhost=vhost, port=port)
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
                node = os.path.join(nginx_conf_dir, container_name)
                os.remove(node)
                call(['/etc/init.d/nginx', 'reload'])

if __name__ == '__main__':
    sys.exit(main())
