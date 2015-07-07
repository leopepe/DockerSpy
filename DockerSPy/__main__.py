#!/bin/env python
__author__ = 'leonardo'

# does it work outsite and inside pycharm?
#from DockerSPy.DockerSpy import DockerSpy
#from DockerSPy.TemplateParser import TemplateParser
from DockerSpy import DockerSpy
from TemplateParser import TemplateParser
from subprocess import call
import os

# constants
PROJECT_DIR = os.path.abspath(os.path.dirname(__file__))
TEMPLATE_DIR = os.path.join(PROJECT_DIR, 'templates')
TEMPLATE_DEFAULT = os.path.join(TEMPLATE_DIR, 'default.conf')
TEMPLATE = os.path.join(TEMPLATE_DIR, 'node.nodomain.conf')


def main():
    docker = DockerSpy()
    parser = TemplateParser(template_path=TEMPLATE)

    # generate config files upon live containers info and using TemplateParser instance
    def node_config_generator():
        data = ''
        # walk through the list of live containers and pass the node infos and generates the node config
        for container_info in docker.live_containers_info():
            node_config_file = '/etc/nginx/conf.d/{0}.conf'.format(container_info['vhost'])
            if container_info['vhost'] and container_info['port']:
                data = parser.replace_node_info(container_info=container_info)
                with open(node_config_file, 'w+') as config_file:
                    config_file.write(data)

    # generate container config during proxy startup
    node_config_generator()

    # Daemonize
    while True:
        for event in docker.event_listener().__iter__():
            if event['status'] == 'start':
                print('Container {name} status changed to {status}'.format(name=event['from'], status=event['status']))
                node_config_generator()
                call(['/etc/init.d/nginx', 'reload'])
            elif event['status'] == 'stop' or event['status'] == 'die':
                print('Container {name} status changed to {status}'.format(name=event['from'], status=event['status']))
                node_config_generator()
                call(['/etc/init.d/nginx', 'reload'])


if __name__ == '__main__':
    main()
