## Getting Started
 
Most of the following content has been taken from official 
[telegram documentation](https://core.telegram.org/bots#6-botfather)
 
Just talk to BotFather (**@botfather**) to receive your authorization token. BotFather is a bot itself. It is used to 
create, delete and perform various actions with other bots. 
 
#### Creating a new bot
Use the `/newbot` command to create a new bot. The BotFather will ask you for a *name* and *username*, then generate an 
*authorization token* for your new bot.

The name of your bot is displayed in contact details and elsewhere.

The Username is a short name, to be used in mentions and `telegram.me` links. Usernames are 5-32 characters 
long and are **case insensitive**, but may only include Latin characters, numbers, and underscores. Your bot's username 
must end in `bot`, e.g. `tetris_bot` or `TetrisBot`.

The token is a string along the lines of `110201543:AAHdqTcvCH1vGWJxfSeofSAs0K5PALDsaw` that is required to authorize the 
bot and send requests to the _Bot API_.

#### Generating an authorization token
If your existing token is compromised or you lost it for some reason, use the `/token` command to generate a new one.