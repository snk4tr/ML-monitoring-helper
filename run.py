import yaml

from ssh_connector import SshConnector


def setup():
    config_path = './config.yaml'
    config = yaml.load(open(config_path, 'r'))
    return config['host'], config['username'], config['password']


def main(host: str, username: str, password: str):
    connector = SshConnector(host, username, password)


if __name__ == "__main__":
    host, username, password = setup()

    main(host, username, password)
