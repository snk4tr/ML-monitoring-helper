import telegram

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters


class Bot:
    def __init__(self, connector, logger, token):
        # init connector
        self.connector = connector
        self.logger = logger

        """Start the bot."""
        # Create the EventHandler and pass it your bot's token.
        updater = Updater(token)

        # Get the dispatcher to register handlers
        dp = updater.dispatcher

        # on different commands - answer in Telegram
        dp.add_handler(CommandHandler("start", self.start))
        dp.add_handler(CommandHandler("help", self.help))
        dp.add_handler(CommandHandler('ls', self.list_files))
        dp.add_handler(CommandHandler('gpu', self.gpu_stat))

        # log all errors
        dp.add_error_handler(self.error)

        # Start the Bot
        updater.start_polling()

        # Run the bot until you press Ctrl-C or the process receives SIGINT,
        updater.idle()
        self.logger.info("SSH ML bot stops its work! Bye! :)")

    def start(self, bot, update):
        """Send a message when the command /start is issued."""
        update.message.reply_text('Hi!')

    def help(self, bot, update):
        """Send helping information about how the bot works when the command /help is issued."""
        chat_id = update.message.chat_id
        reply = 'There are a few pretty useful commands for you to try:\n/gpu - provides *gpustat*-like info about ' \
                'current work machine load.\n/ls - performs plain old *ls* command (lists files in current directory).'
        bot.send_message(chat_id=chat_id,
                         text=reply,
                         parse_mode=telegram.ParseMode.MARKDOWN)

    def error(self, update, error):
        """Log Errors caused by Updates."""
        self.logger.warning('Update "%s" caused error "%s"', update, error)

    def list_files(self, bot, update):
        """List files in current directory"""
        reply = self.connector.list_files()
        update.message.reply_text(reply)

    def gpu_stat(self, bot, update):
        """Provide detailed information about current GPU usage."""
        chat_id = update.message.chat_id
        degree_sign = u'\N{DEGREE SIGN}'
        name, util, usedm, totalm, temp = self.connector.gpu_stat()
        reply = ''
        reply += '`' + str(name) + '`\n'
        reply += '*Utilization*: ' + str(util) + ' / ' + '100%\n'
        reply += '*Memory*: ' + str(usedm) + ' / ' + str(totalm) + ' MB\n'
        reply += '*Temperature*: `' + str(temp) + degree_sign + 'C`'
        bot.send_message(chat_id=chat_id,
                         text=reply,
                         parse_mode=telegram.ParseMode.MARKDOWN)
