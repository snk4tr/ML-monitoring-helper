# ML monitoring helper
Telegram bot made to simplify management of Machine Learning and Deep Learing routines. 
You may find it useful to aggregate information about learning processes from multiple 
remote machines into a single telegram channel. If so checkout this repo :bowtie: 

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development, testing or 
usage purposes.

### Prerequisites

* docker `18.06.0+` :white_check_mark:
* docker-compose `1.22.0+` :white_check_mark:

### Installing

1. Clone this repository on your local machine:  
`$ git clone https://github.com/snk4tr/ML-monitoring-helper.git`
2. Follow a [few simple steps](https://core.telegram.org/bots#6-botfather) to get 
access token. You may have telegram site blocked for some reason. If so please follow 
instructions provided [here](docs/getting_started.md).
3. Create `config.yaml` file based on `config-template.yaml`. Fill it with
you personal info and set of parameters you prefer.
4. Run the docker container, it will do all the work:  
`$ docker-compose up`  

## Commands

* `/help` - informs about available commands.
* `/gpu` - provides **gpustat**-like info about current work machine load.
* `/ls` - performs plain old **ls** command (lists files in current directory).
* `/watch` - **enables and disables** watching for learning on target machine.
* `/stop` - deactivates the bot (**does not** stop the bot app itself❗).

## Built with

* [python-telegram-bot](https://github.com/python-telegram-bot/python-telegram-bot) - wrapper over 
[Telegram Bot API](https://core.telegram.org/bots/api).
* [parallel-ssh](https://pypi.org/project/parallel-ssh/) - asynchronous parallel SSH client library.

### Versioning

[SemVer](https://semver.org) is used for versioning. For the versions available, see the 
[tags on this repository](https://github.com/snk4tr/ML-monitoring-helper/releases).

### License

This project is licensed under the Apache License 2.0 - see the [LICENSE](LICENSE) file for details.

### Authors

* **Sergey Kastryulin** - _Initial work_ - [snk4tr](https://github.com/snk4tr)


