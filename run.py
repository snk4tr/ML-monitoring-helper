import yaml

from src.ssh_connector import SshConnector
from src.bot import Bot


def setup():
    config_path = './config.yaml'
    config = yaml.load(open(config_path, 'r'))
    return config['host'], config['port'], config['username'], config['password'], config['token']


def main():
    host, port, username, password, token = setup()
    print('Setup finished!')
    connector = SshConnector(host, port, username, password)
    print('Connection finished!')
    bot = Bot(connector, token)


if __name__ == '__main__':
    main()
