import json
from pssh.clients import ParallelSSHClient


class SshConnector:
    def __init__(self, host, port, username, password, logger):
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.logger = logger
        self.client = self.connect()

    def connect(self):
        """
        Establishes connection with remote machine.
        Returns:
            (ParallelSSHClient) ssh connection object.
        """
        try:
            return ParallelSSHClient(
                hosts=[self.host], port=self.port, user=self.username, password=self.password)

        except AuthenticationException as e:
            print('Authentication failure! Credentials must be wrong!', e)

    def list_files(self):
        assert self.client is not None, "Connection object has not been initialized!"
        output = self.client.run_command('ls')

        out = ''
        for host, host_out in output.items():
            for line in host_out.stdout:
                out += line + ' '
        return out

    def gpu_stat(self):
        assert self.client is not None, "Connection object has not been initialized!"
        output = self.client.run_command('gpustat --json')
        data = self.__parse_gpu_stat(output)

        name = data['gpus'][0]['name']
        util = data['gpus'][0]['utilization.gpu']
        usedm = data['gpus'][0]['memory.used']
        totalm = data['gpus'][0]['memory.total']
        temp = data['gpus'][0]['temperature.gpu']
        return name, util, usedm, totalm, temp

    def __parse_gpu_stat(self, output):
        out = ""
        for host, host_out in output.items():
            for line in host_out.stdout:
                out += line + " "
        return json.loads(out)