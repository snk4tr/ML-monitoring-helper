import json

from pssh.clients import ParallelSSHClient
from src.util.parser import parse_output


class SshConnector:
    def __init__(self, host, port, username, password, logger):
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.logger = logger

        # Initialise ssh connection with client.
        self.client = self.connect()

    def connect(self):
        """
        Establishes connection with remote machine.
        Returns:
            (ParallelSSHClient) ssh connection object.
        """
        try:
            connection = ParallelSSHClient(
                hosts=[self.host], port=self.port, user=self.username, password=self.password)
            self.logger.info('SSH connection has been successfully established.')
            return connection

        except AuthenticationException as e:
            self.logger.exception('Authentication failure! Credentials must be wrong!')
            exit(1)

    def list_files(self):
        """
        Lists files in current directory.
        Returns:
            (str) string including all names of all files in directory.
        """
        assert self.client is not None, "Connection object has not been initialized!"
        output = self.client.run_command('ls')
        return parse_output(output)

    def get_gpu_stat(self):
        """
        Retrieves information about current GPU state from `gpustat` util, parses it and gives further.
        Returns:
            (str, int, int, int) several useful characteristics of current GPU state.
        """
        assert self.client is not None, "Connection object has not been initialized!"
        output = self.client.run_command('gpustat --json')
        data = json.loads(parse_output(output))

        # Retrieve all useful information about GPU state.
        name = data['gpus'][0]['name']
        util = data['gpus'][0]['utilization.gpu']
        usedm = data['gpus'][0]['memory.used']
        totalm = data['gpus'][0]['memory.total']
        temp = data['gpus'][0]['temperature.gpu']
        return name, util, usedm, totalm, temp
