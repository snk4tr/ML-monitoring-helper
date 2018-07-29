# telegram-ssh-ml
Telegram bot made to simplify management of ML and DL routines.

### Prerequisites

* docker `18.06.0`+ :white_check_mark:

## Getting Started

1. Follow a [few simple steps](https://core.telegram.org/bots#6-botfather) to get 
access token.
2. Create `config.yaml` file based on `config-template.yaml`. Fill it with
you personal info and set of parameters you prefer.
3. `$ docker-compose up`  

## Commands

* `/help` - informs about available commands.
* `/gpu` - provides **gpustat**-like info about current work machine load.
* `/ls` - performs plain old **ls** command (lists files in current directory).
* `/watch` - **enables and disables** watching for learning on target machine.
* `/stop` - deactivates the bot (**does not** stop the bot app itself❗).