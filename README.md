# DockerSpy

The purpose of the project is to implement a service that inspects the Docker API and provides a dynamic configurator for nginx reverse proxy.

DockerSpy expects that each container being bring up will set an environment variable exposing the virtual host and virtual port.

## Install

Choose an empty directory and run the commands below to install it.
 
  $ cd /tmp
  $ git clone https://github.com/leopepe/DockerSpy.git
  $ cd dockerspy ; python setup.py install

## Usage

To start the dockerspy process in foreground:

   $ dockerspy -u 'unix://var/run/docker.sock' -o '/etc/nginx/conf.d/' -t 'templates/node.nodomain.conf'

It will start in foreground and locks the terminal. Use '&' to send it to background or use it with a process supervisory system such as Supervisor, Circus, forego etc.

## TODO

- PyDocs
- System logging

## Release: 1.0
- The containers must be bring up with 2 environment variables VIRTUAL_HOST and VIRTUAL_PORT
- The solution supports only 1 port per docker
- Access to docker.sock is necessary in due to access docker api
- Flexible template usage. Users can use -t option in CLI to specify the template file to be used to generate the config
 files for nodes.
- Config and Args parser
- Proper python distribution package
