from pssh.clients import ParallelSSHClient


class SshConnector:
    def __init__(self, host, port, username, password):
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.client = None

    def connect(self):
        try:
            self.client = ParallelSSHClient(
                hosts=[self.host], port=self.port, user=self.username, password=self.password)

        except AuthenticationException as e:
            print('Authentication failure! Credentials must be wrong!', e)

    def list_files(self):
        assert self.client is not None, "Connection object has not been initialized!"
        output = self.client.run_command('ls')

        for host, host_out in output.items():
            for line in host_out.stdout:
                print(line)
