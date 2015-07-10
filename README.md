# DockerSpy

The purpose of the project is to implement a service that inspects the Docker API and provides a dynamic configurator for nginx reverse proxy.

DockerSpy expects that each container being bring up will set an environment variable exposing the virtual host and virtual port.

## Usage
Up to now the application must be bring up using:

   $ python3 -m DockerSpy -u 'unix://var/run/docker.sock' -o '/etc/nginx/conf.d/' -t '/home/leonardo/PycharmProjects/DockerSPy/DockerSpy/templates/node.nodomain.conf'

It will start in foreground and locks the terminal. Use '&' to send it to background or use it with a process supervisory system such as Supervisor, Circus, forego etc.

## TODO

- PyDocs
- System logging
- Proper python distribution package

## Release: 1.0
- The containers must be bring up with 2 environment variables VIRTUAL_HOST and VIRTUAL_PORT
- The solution supports only 1 port per docker
- Access to docker.sock is necessary in due to access docker api
- Flexible template usage. Users can use -t option in CLI to specify the template file to be used to generate the config
 files for nodes.
- Config and Args parser