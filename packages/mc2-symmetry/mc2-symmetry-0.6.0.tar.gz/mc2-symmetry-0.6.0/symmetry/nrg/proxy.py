import jinja2

from symmetry.common.ssh import Connection


class NginxProxyConfigurator:
    _template_string = '''
        location /{{ service_id }} {
            rewrite ^/{{ service_id }}/(.*)$ /$1 break;
            rewrite ^/{{ service_id }}(.*)$ /$1 break;
            proxy_pass         http://{{ host }}:{{ service_port }};
            proxy_redirect     off;
            proxy_set_header   Host $host;
            proxy_set_header   X-Real-IP $remote_addr;
            proxy_set_header   X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header   X-Forwarded-Host $server_name;
        }
    '''
    _template: jinja2.Template

    def __init__(self) -> None:
        super().__init__()
        self._template = jinja2.Environment(loader=jinja2.BaseLoader()).from_string(self._template_string)

    def list_existing_entries(self, node_ip):
        with Connection(node_ip, username='root') as ssh:
            result = ssh.run('find /etc/nginx/symmetry -name "*.conf" -printf "%f\n"')
            return [entry.rstrip('.conf') for entry in result.result.split('\n')]

    def create_entry(self, node_ip, service_id, service_port):
        with Connection(node_ip, username='root') as ssh:
            ssh.open_sftp()
            ssh.change_sftp_dir(path='/etc/nginx/symmetry')

            new_config = self._render_config(service_id, service_port)

            with ssh.get_sftp_file('%s.conf' % service_id, mode='w') as config:
                config.write(new_config)

            ssh.run('nginx -s reload')

    def remove_entry(self, node_ip, service_id):
        if not service_id:
            raise ValueError
        if service_id == '*':
            raise ValueError

        with Connection(node_ip, username='root') as ssh:
            try:
                ssh.run('rm -f /etc/nginx/symmetry/%s.conf && nginx -s reload' % service_id)
            finally:
                ssh.close()

    def _render_config(self, service_id, service_port, host='localhost'):
        return self._template.render(host=host, service_id=service_id, service_port=service_port)