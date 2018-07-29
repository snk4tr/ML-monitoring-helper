import telegram

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters


class Bot:
    def __init__(self, connector, logger, token):
        # Init util objects and constants
        self.connector = connector
        self.logger = logger
        self.WATCH_FREQ = 1  # seconds

        # Init bot state
        self.watching = False
        self.learning = False

        # Create the EventHandler and pass it your bot's token.
        updater = Updater(token)
        job = updater.job_queue

        # Get the dispatcher to register handlers
        dp = updater.dispatcher

        # On different commands - answer in Telegram
        dp.add_handler(CommandHandler("start", self.start))
        dp.add_handler(CommandHandler("help", self.help))
        dp.add_handler(CommandHandler('ls', self.list_files))
        dp.add_handler(CommandHandler('gpu', self.get_gpu_stat))
        dp.add_handler(CommandHandler('watch', self.watch_learning, pass_job_queue=True))

        dp.add_handler(MessageHandler(Filters.command, self.unknown))

        # Log all errors
        dp.add_error_handler(self.error)

        # Start the Bot
        updater.start_polling()

        # Run the bot until you press Ctrl-C or the process receives SIGINT,
        try:
            updater.idle()
        except KeyboardInterrupt:
            self.logger.info("SSH ML bot stops its work! Bye! :)")
        finally:
            self.finish_work()

    def start(self, bot, update):
        """Send a message when the command /start is issued."""
        update.message.reply_text('Hi!')

    def help(self, bot, update):
        """Send helping information about how the bot works when the command /help is issued."""
        chat_id = update.message.chat_id
        reply = 'There are a few pretty useful commands for you to try:\n\n/gpu - provides *gpustat*-like info about ' \
                'current work machine load.\n/ls - performs plain old *ls* command (lists files in current directory).'
        bot.send_message(chat_id=chat_id,
                         text=reply,
                         parse_mode=telegram.ParseMode.MARKDOWN)

    def error(self, update, error):
        """Log Errors caused by Updates."""
        self.logger.warning('Update "%s" caused error "%s"', update, error)

    def unknown(self, bot, update):
        bot.send_message(chat_id=update.message.chat_id, text="Sorry, I didn't understand that command.")

    def list_files(self, bot, update):
        """List files in current directory"""
        reply = self.connector.list_files()
        update.message.reply_text(reply)

    def get_gpu_stat(self, bot, update):
        """Provide detailed information about current GPU usage."""
        chat_id = update.message.chat_id
        degree_sign = u'\N{DEGREE SIGN}'
        name, util, usedm, totalm, temp = self.connector.get_gpu_stat()
        reply = ''
        reply += '`' + str(name) + '`\n'
        reply += '*Utilization*: ' + str(util) + ' / ' + '100%\n'
        reply += '*Memory*: ' + str(usedm) + ' / ' + str(totalm) + ' MB\n'
        reply += '*Temperature*: `' + str(temp) + degree_sign + 'C`'
        bot.send_message(chat_id=chat_id, text=reply, parse_mode=telegram.ParseMode.MARKDOWN)

    def watch_learning(self, bot, update, job_queue):
        chat_id = update.message.chat_id
        self.watching = not self.watching
        if self.watching:
            bot.send_message(chat_id=chat_id, text='Monitoring of learning has been started!')
            job_queue.run_repeating(self.__watch, self.WATCH_FREQ, context=update.message.chat_id)
            return
        # Temporarily disable monitoring
        bot.send_message(chat_id=chat_id, text='Monitoring of learning has been stopped!')
        job_queue.enabled = self.watching

    def __watch(self, bot, job):
        _, util, usedm, totalm, _ = self.connector.get_gpu_stat()
        mem_thresh = usedm / totalm
        if not self.learning and mem_thresh > 0.9 and util > 10:
            self.learning = not self.learning
            bot.send_message(chat_id=job.context, text='Learning started!')

        if self.learning and mem_thresh < 0.9 and util < 10:
            self.learning = not self.learning
            bot.send_message(chat_id=job.context, text='Learning finished!')

    def finish_work(self, bot, update):
        chat_id = update.message.chat_id
        bot.send_message(chat_id=chat_id, text='Bye!', parse_mode=telegram.ParseMode.MARKDOWN)
