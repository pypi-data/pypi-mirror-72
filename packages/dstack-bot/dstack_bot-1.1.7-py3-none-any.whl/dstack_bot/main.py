#!/usr/bin/env python
# -*- coding: utf-8 -*-
import logging
import re

import dotenv
from invoke import run
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, TelegramError
from telegram.ext import CallbackQueryHandler, CommandHandler, Filters, Updater

from dstack_bot.tasks import cleanup
from .exceptions import NotConfigured
from .utils import get_env, stats_summary

dotenv.load_dotenv(dotenv.find_dotenv())

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger('dstack_cubed')

envs = [
    'TELEGRAM_BOT_TOKEN',
    'TELEGRAM_BOT_ADMIN1',
    'TELEGRAM_BOT_ADMIN2',
    'S3_BUCKET_NAME',
    'S3_BACKUP_PATH',
    'S3_BACKUP_TAG',
    'LOCAL_BACKUP_PATH',
    'POSTGRES_CONTAINER_NAME',
    'POSTGRES_USERNAME',
]

try:
    token = get_env('TELEGRAM_BOT_TOKEN')
    admin1 = Filters.user(username=get_env('TELEGRAM_BOT_ADMIN1'))
    admin2 = Filters.user(username=get_env('TELEGRAM_BOT_ADMIN2'))
except NotConfigured as e:
    raise TelegramError(str(e))


def run_and_reply(update, command, reply=True, process_func=None, pty=False):
    """Initial implementation of message response that support paging if message is too long

    """
    result = run(command, hide=True, warn=True, pty=pty)
    if process_func and result.stdout:
        message = process_func(result.stdout)
        if not reply:
            return message
    else:
        message = result.stdout or result.stderr or "No output."
    if len(message) < 4096:  # max Telegram message length
        update.message.reply_markdown(f'```bash\n{message}\n```')
    else:
        max_length = 4096
        message_parts = [message[i:i + max_length] for i in range(0, len(message), max_length)]
        # restrict to only two messages and truncate rest to prevent flooding Telegram
        for message in message_parts[:2]:
            update.message.reply_markdown(f'```bash\n{message}\n```')
        if len(message_parts) > 2:
            update.message.reply_markdown(f'```bash\n...message truncated...\n```')


# Define a few command handlers. These usually take the two arguments bot and
# update. Error handlers also receive the raised TelegramError object in error.
def start(bot, update):
    """Send a message when the command /start is issued."""
    update.message.reply_text("""
    Available commands:
    /start        - shows this help
    /status       - checks the status of the toolset service
    /stats        - shows server stats
    /restart      - interactively restart docker services running on host
    /users        - download csv of the current users
    /backup       - create backup and upload to s3 bucket
    /show_backups - show list of most recent backups
    /shell        - run arbitrary commands using dstack/invoke on the server.
    """)


def invoke(bot, update):
    """Run message as invoke task"""
    run_and_reply(update, update.message.text[7:], pty=True)


def status(bot, update):
    """Run message as invoke task"""
    run_and_reply(update, "docker ps --format 'table {{.Names}}\t{{.Status}}'")


def error(bot, update, error_name):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, error_name)
    update.message.reply_markdown(f'```bash\n{error_name}\n```')


def stats(bot, update):
    update.message.reply_markdown(f'```bash\n{stats_summary()}\n```')


def users(bot, update):
    try:
        container_name = get_env('POSTGRES_CONTAINER_NAME')
        postgres_username = get_env('POSTGRES_USERNAME')
    except NotConfigured as e:
        raise TelegramError(str(e))
    path = '/tmp/users.csv'
    fields = ['username', 'email', 'first_name', 'last_name']
    update.message.reply_text('Download file below:')
    run(f'docker exec {container_name} psql -U {postgres_username} -c "'
        f"COPY (select {','.join(fields)} from auth_user) to '{path}' (format csv, delimiter ',');"
        '"', hide=True, warn=True, pty=False)
    run(f'docker cp {container_name}:{path} {path}', hide=True, warn=True, pty=False)
    bot.send_document(chat_id=update.message.chat_id, document=open('/tmp/users.csv', 'rb'))


def backup(bot, update):
    """Run message as invoke task"""
    tag = get_env('S3_BACKUP_TAG') or update.message.text[7:]
    run_and_reply(update, f'dstack e db backup --tag {tag}')
    cleanup('*.tar.gz')


def show_backups(bot, update):
    try:
        bucket = get_env('S3_BUCKET_NAME')
        backup_path = get_env('S3_BACKUP_PATH')
        endpoint_url = get_env('ENDPOINT_URL')
    except NotConfigured as exception:
        raise TelegramError(str(exception))

    def _process(stdout):
        backups = []
        aws_ls = stdout.split('\n')
        for entry in aws_ls[:-1]:
            match = re.match('.+db_backup\.(?P<date>[\dT-]{19}Z)_(?P<tag>.+)\.tar\.gz$', entry)
            if match:
                data = match.groupdict()
                backups.append(f"{data['date']} - {data['tag']}")
        backups.reverse()
        message = '\n'.join(backups[:5])
        return message

    run_and_reply(update, f'aws --endpoint-url={endpoint_url} s3 ls s3://{bucket}{backup_path}', process_func=_process)


def restart(bot, update):
    services = run_and_reply(update, "docker ps --format '{{.Names}}'",
                             reply=False, process_func=lambda s: s.split('\n')[:-1])
    width = 3

    def _button(service):
        return InlineKeyboardButton(service.split('_')[1].title(), callback_data=service)

    keyboard = [[_button(service) for service in services[width * row:width * (row + 1)]
                 ] for row in range(len(services) // width + (1 if len(services) % width else 0))]

    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_markdown('Select service to restart:', reply_markup=reply_markup)


def restart_service(bot, update):
    query = update.callback_query
    service = query.data
    result = run(f'docker restart {service}', hide=True, warn=True, pty=False)
    if result.stdout:
        message = f'{service} restarted'
    else:
        message = result.stderr or "No output."
    bot.edit_message_text(text=message, chat_id=query.message.chat_id, message_id=query.message.message_id)


def main():
    """Start the bot."""
    # Create the EventHandler and pass it your bot's token.
    updater = Updater(token)
    # Get the dispatcher to register handlers
    dp = updater.dispatcher
    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start, filters=admin1 | admin2))
    dp.add_handler(CommandHandler("help", start, filters=admin1 | admin2))
    dp.add_handler(CommandHandler("shell", invoke, filters=admin1 | admin2))
    dp.add_handler(CommandHandler("status", status, filters=admin1 | admin2))
    dp.add_handler(CommandHandler("stats", stats, filters=admin1 | admin2))
    dp.add_handler(CommandHandler("restart", restart, filters=admin1 | admin2))
    dp.add_handler(CommandHandler("backup", backup, filters=admin1 | admin2))
    dp.add_handler(CommandHandler("users", users, filters=admin1 | admin2))
    dp.add_handler(CommandHandler("show_backups", show_backups, filters=admin1 | admin2))
    # on non-command i.e message - echo the message on Telegram
    # dp.add_handler(MessageHandler(Filters.text & (admin1 | admin2), invoke))
    # TODO: Make sure this is secure
    dp.add_handler(CallbackQueryHandler(restart_service))
    # log all errors
    dp.add_error_handler(error)
    # Start the Bot
    updater.start_polling()
    logger.info('Bot started')
    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
