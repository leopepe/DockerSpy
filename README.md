# DockerSpy

The pourpose of the project is to implement a service that inspects the Docker API and provides a dynamic configurator for nginx reverse proxy.

DockerSpy expects that each container being bring up will set an environment variable exposing the virtual host and virtual port.
