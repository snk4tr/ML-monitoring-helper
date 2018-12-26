import yaml
import logging

from datetime import datetime
from src.ssh_connector import SshConnector
from src.bot import Bot
from logging.handlers import RotatingFileHandler


def init_config(config_path: str) -> dict:
    with open(config_path, 'r') as f:
        config = yaml.load(f)

    return config


def init_logger(config: dict) -> logging.Logger:
    log_formatter = logging.Formatter('%(asctime)s %(levelname)s %(funcName)s(%(lineno)d) %(message)s')
    handler = RotatingFileHandler(filename=datetime.now().strftime('%H_%M_%d_%m_%Y.log'),
                                  mode='a',
                                  maxBytes=100*1024*1024,  # 100 Mb
                                  backupCount=2,
                                  encoding=None,
                                  delay=0)
    handler.setFormatter(log_formatter)
    handler.setLevel(logging.INFO)

    logger = logging.getLogger('root')
    logger.setLevel(logging.INFO)
    logger.addHandler(handler)

    return logger


def main():
    config_path = './config.yaml'
    config = init_config(config_path)
    logger = init_logger(config)
    connector = SshConnector(config['host'], config['port'], config['username'], config['password'], logger)

    # running bot
    Bot(connector, logger, config)


if __name__ == '__main__':
    main()
