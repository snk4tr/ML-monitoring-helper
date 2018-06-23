import yaml

from ssh_connector import SshConnector


def setup():
    config_path = './config.yaml'
    config = yaml.load(open(config_path, 'r'))
    return config['host'], config['port'], config['username'], config['password']


def main(host: str, port: str, username: str, password: str):
    connector = SshConnector(host, port, username, password)
    connector.connect()
    connector.list_files()


if __name__ == "__main__":
    host, port, username, password = setup()

    main(host, port, username, password)
