__author__ = 'leonardo'

class TemplateParser:
    """

        parser = TemplateParser()
        container_info = {}
        container_info = {
            'name': 'node1',
            'vhost': 'node1.nodomain',
            'ip': '172.0.10.5',
            'port': '8080'
        }
        print(parser.replace_node_info(container_info=container_info))

    """
    def __init__(self, template_path='./templates/nginx-https_offload_management_redirect-sample-1.0.conf'):
        self.template_data = None
        with open(template_path, 'r') as template_file:
            self.template_data = template_file.read()

    def replace_data(self, **kwargs):
        data = self.template_data.replace(
            '<container_vhost>', kwargs.get('vhost', '')
        ).replace(
            '<container_ip>', kwargs.get('ip', '')
        ).replace(
            '<container_port>', kwargs.get('port', '')
        )
        return data
