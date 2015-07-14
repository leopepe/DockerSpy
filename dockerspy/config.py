__author__ = 'leonardo'

import argparse
from dockerspy import name


def configurator():
    parser = argparse.ArgumentParser(prog=name, description='dockerspy agent options and arguments')
    parser.add_argument('-t', '--template',
                        dest='template_path',
                        help='Template file to be used as base to generate the cluster node config.',
                        default='node.nodomain.conf')
    parser.add_argument('-o', '--output-directory',
                        dest='output_dir',
                        help='Full path where config files must be generated.',
                        default='/etc/nginx/conf.d/')
    parser.add_argument('-u', '--url',
                        dest='api_url',
                        help='Docker API url. Default is unix domain socket /var/run/docker.sock;',
                        default='unix://var/run/docker.sock')

    return parser

