from src.ssh_connector import SshConnector


def construct_gpu_stat_reply(connector: SshConnector) -> str:
    degree_sign = u'\N{DEGREE SIGN}'
    name, util, usedm, totalm, temp = connector.get_gpu_stat()
    reply = ''
    reply += '`' + str(name) + '`\n'
    reply += '*Utilization*: ' + str(util) + ' / ' + '100%\n'
    reply += '*Memory*: ' + str(usedm) + ' / ' + str(totalm) + ' MB\n'
    reply += '*Temperature*: `' + str(temp) + degree_sign + 'C`'
    return reply


def construct_help_reply() -> str:
    reply = 'There are a few pretty useful commands for you to try:🔍\n\n' \
            '/help - informs about available commands.\n' \
            '/gpu - provides *gpustat*-like info about current work machine load.\n' \
            '/ls - performs plain old *ls* command (lists files in current directory).\n' \
            '/watch - *enables and disables* watching for learning on target machine.\n' \
            '/stop - deactivates the bot (*does not* stop the bot app itself❗).'
    return reply
