import logging

from src.ssh_connector import SshConnector
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters


class Bot:
    def __init__(self, connector, token):
        logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                            level=logging.INFO)
        # Enable logging
        self.logger = logging.getLogger(__name__)

        print('Inside Bot: logging has been set')
        # init connector
        self.connector = connector
        print('Inside Bot: connector has been initialized')

        """Start the bot."""
        # Create the EventHandler and pass it your bot's token.
        updater = Updater(token)

        # Get the dispatcher to register handlers
        dp = updater.dispatcher

        # on different commands - answer in Telegram
        dp.add_handler(CommandHandler("start", self.start))
        dp.add_handler(CommandHandler("help", self.help))
        dp.add_handler(CommandHandler('ls', self.ls))

        # on noncommand i.e message - echo the message on Telegram
        dp.add_handler(MessageHandler(Filters.text, self.echo))

        # log all errors
        dp.add_error_handler(self.error)

        # Start the Bot
        updater.start_polling()
        print('Inside Bot: after start polling')

        # Run the bot until you press Ctrl-C or the process receives SIGINT,
        # SIGTERM or SIGABRT. This should be used most of the time, since
        # start_polling() is non-blocking and will stop the bot gracefully.
        print('Inside Bot: before idle')
        updater.idle()
        print('Inside Bot: after idle')

    # Define a few command handlers. These usually take the two arguments bot and
    # update. Error handlers also receive the raised TelegramError object in error.
    def start(self, bot, update):
        """Send a message when the command /start is issued."""
        update.message.reply_text('Hi!')

    def help(self, bot, update):
        """Send a message when the command /help is issued."""
        update.message.reply_text('Help!')

    def echo(self, bot, update):
        """Echo the user message."""
        update.message.reply_text(update.message.text)

    def error(self, bot, update, error):
        """Log Errors caused by Updates."""
        self.logger.warning('Update "%s" caused error "%s"', update, error)

    def ls(self, bot, update):
        reply = self.connector.list_files()
        update.message.reply_text(reply)


