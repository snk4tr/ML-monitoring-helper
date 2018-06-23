from pssh.clients import ParallelSSHClient


class SshConnector:
    def __init__(self, host, username, password):
        self.host = host
        self.username = username
        self.password = password
        self.client = None

    def connect(self):
        try:
            self.client = ParallelSSHClient(hosts=[self.host], user=self.username, password=self.password)

        except AuthenticationException as e:
            print('Authentication failure!', e)

    def list_files(self):
        output = self.client.run_command('ls -la')

        for host, host_out in output.items():
            for line in host_out.stdout:
                print(line)
