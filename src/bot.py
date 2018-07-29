import telegram
import time

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from src.util.text_bulder import construct_gpu_stat_reply, construct_help_reply


class Bot:
    def __init__(self, connector, logger, config):
        self.connector = connector
        self.logger = logger
        self.config = config
        self.mem_thresh = float(self.config.get('mem_thresh'))
        self.util_thresh = int(self.config.get('util_thresh'))

        # Init bot state
        self.watching = False
        self.is_learning = False
        self.start_learning_time = None

        # Create the EventHandler and pass it your bot's token.
        self.updater = Updater(config['token'])
        job = self.updater.job_queue
        # Get the dispatcher to register handlers.
        dp = self.updater.dispatcher
        self.__set_handlers(dp)

        # Start the Bot
        self.updater.start_polling()

        # Run the bot until you press Ctrl-C or the process receives SIGINT.
        self.updater.idle()
        self.logger.info("SSH ML bot stops its work! Bye! :)")

    def __set_handlers(self, dp):
        """On different commands - answer in Telegram."""
        dp.add_handler(CommandHandler("help", self.help))
        dp.add_handler(CommandHandler('ls', self.list_files))
        dp.add_handler(CommandHandler('gpu', self.get_gpu_stat))
        dp.add_handler(CommandHandler('watch', self.watch_learning, pass_job_queue=True))
        dp.add_handler(CommandHandler('stop', self.stop_bot))
        dp.add_handler(MessageHandler(Filters.command, self.unknown))
        dp.add_error_handler(self.error)

    def help(self, bot, update):
        """Send helping information about how the bot works when the command /help is issued."""
        chat_id = update.message.chat_id
        reply = construct_help_reply()
        bot.send_message(chat_id=chat_id, text=reply, parse_mode=telegram.ParseMode.MARKDOWN)

    def error(self, update, error):
        """Log Errors caused by Updates."""
        self.logger.warning('Update "%s" caused error "%s"', update, error)

    def unknown(self, bot, update):
        bot.send_message(chat_id=update.message.chat_id, text="Sorry, I didn't understand that command 🆘")

    def list_files(self, bot, update):
        """List files in current directory."""
        reply = self.connector.list_files()
        update.message.reply_text(reply)

    def get_gpu_stat(self, bot, update):
        """Provide detailed information about current GPU usage."""
        chat_id = update.message.chat_id
        reply = construct_gpu_stat_reply(self.connector)
        bot.send_message(chat_id=chat_id, text=reply, parse_mode=telegram.ParseMode.MARKDOWN)

    def watch_learning(self, bot, update, job_queue):
        """Start/stop monitoring or learning on the remote machine."""
        chat_id = update.message.chat_id
        self.watching = not self.watching
        if self.watching:
            bot.send_message(chat_id=chat_id, text='Monitoring of learning has been started!📡')
            job_queue.run_repeating(self.__watch, self.config.get('watch_freq'), context=update.message.chat_id)
            return
        bot.send_message(chat_id=chat_id, text='Monitoring of learning has been stopped❗️❌')
        job_queue.enabled = self.watching

    def __watch(self, bot, job):
        """Periodically check whether learning has been started/stopped."""
        _, util, usedm, totalm, _ = self.connector.get_gpu_stat()
        mem_usage = usedm / totalm
        if not self.is_learning and mem_usage > self.mem_thresh and util > self.util_thresh:
            self.__start_learning(bot, job)
        if self.is_learning and mem_usage < self.mem_thresh and util < self.util_thresh:
            self.__stop_learning(bot, job)

    def __learning_stopped(self, mem_usage, util):
        return not self.is_learning and mem_usage > self.mem_thresh and util > self.util_thresh

    def __stop_learning(self, bot, job):
        self.is_learning = not self.is_learning
        secs = time.time() - self.start_learning_time
        hrs, mns, secs = int(secs // 3600), (int(secs // 60)) % 60, int(secs % 60)
        text = f'🔚 Learning finished!🎉  It took *{hrs} hours {mns} minutes {secs} seconds*❗️'
        bot.send_message(chat_id=job.context, text=text, parse_mode=telegram.ParseMode.MARKDOWN)

    def __start_learning(self, bot, job):
        self.is_learning = not self.is_learning
        bot.send_message(chat_id=job.context, text='Learning started❗️🔜🙏')
        self.start_learning_time = time.time()

    def stop_bot(self, bot, update):
        """Make bot inactive. The program will still be running though"""
        chat_id = update.message.chat_id
        text = 'Bot is finishing its work. See ya! 😏'
        bot.send_message(chat_id=chat_id, text=text, parse_mode=telegram.ParseMode.MARKDOWN)
        self.updater.stop()
