import yaml
import logging

from src.ssh_connector import SshConnector
from src.bot import Bot


def main():
    config_path = './config.yaml'
    config = yaml.load(open(config_path, 'r'))
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                        level=logging.INFO)
    logger = logging.getLogger(__name__)
    connector = SshConnector(config['host'], config['port'], config['username'], config['password'], logger)

    # running bot
    Bot(connector, logger, config)


if __name__ == '__main__':
    main()
