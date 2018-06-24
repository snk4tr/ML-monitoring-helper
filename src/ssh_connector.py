import json
from pssh.clients import ParallelSSHClient


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
            return ParallelSSHClient(
                hosts=[self.host], port=self.port, user=self.username, password=self.password)

        except AuthenticationException as e:
            print('Authentication failure! Credentials must be wrong!', e)

    def list_files(self):
        """
        Lists files in current directory.
        Returns:
            (str) string including all names of all files in directory.
        """
        assert self.client is not None, "Connection object has not been initialized!"
        output = self.client.run_command('ls')
        return self.__parse_output(output)

    def gpu_stat(self):
        """
        Retrieves information about current GPU state from `gpustat` util, parses it and gives further.
        Returns:
            (str, int, int, int) several useful characteristics of current GPU state.
        """
        assert self.client is not None, "Connection object has not been initialized!"
        output = self.client.run_command('gpustat --json')
        data = json.loads(self.__parse_output(output))

        # Retrieve all useful information about GPU state.
        name = data['gpus'][0]['name']
        util = data['gpus'][0]['utilization.gpu']
        usedm = data['gpus'][0]['memory.used']
        totalm = data['gpus'][0]['memory.total']
        temp = data['gpus'][0]['temperature.gpu']

        return name, util, usedm, totalm, temp

    @staticmethod
    def __parse_output(output):
        """
        Parses console outputs of performed commands.
        Args:
            output (dict): dict, a part of which may be used as a generator object (host_out.stdout) for retrieving
            lines of console output.
        Returns:
            (str) sting of all console output.
        """
        out = ""
        for host, host_out in output.items():
            for line in host_out.stdout:
                out += line + " "
        return out
