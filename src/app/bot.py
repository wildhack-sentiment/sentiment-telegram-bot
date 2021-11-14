import logging
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, Update
from telegram.ext import CallbackContext, CallbackQueryHandler, CommandHandler, Dispatcher, Filters, MessageHandler

from app.models import Command, TelegramUser
from app.report import generate_report

logger = logging.getLogger(__name__)

reply_keyboard = ReplyKeyboardMarkup([['ℹ️ О сервисе']], resize_keyboard=True)
select_report_markup = InlineKeyboardMarkup([
    [InlineKeyboardButton('Отчет по товару 1', callback_data='keyboard_report_1')],
    [InlineKeyboardButton('Отчет по товару 2', callback_data='keyboard_report_2')],
    [InlineKeyboardButton('Отчет по товару 3', callback_data='keyboard_report_3')],
    [InlineKeyboardButton('Отчет по товару 4', callback_data='keyboard_report_4')],
])


def process_event(event, user):
    logger.info(event)


def user_get_by_update(update: Update):
    if update.message:
        message = update.message
    else:
        message = update.callback_query.message

    full_name = ''
    if message.chat.first_name:
        full_name += message.chat.first_name
    if message.from_user.last_name:
        full_name += ' ' + message.chat.last_name

    instance, created = TelegramUser.objects.update_or_create(
        chat_id=message.chat.id,
        defaults={
            'chat_id': message.chat.id,
            'user_name': message.chat.username,
            'full_name': full_name,
        },
    )

    return instance


def process_command(name, user, text=''):
    slug_list = {
        'Started bot': 'help_start',
        'Sent command "Help analyse category"': 'help_analyse_category',
        'Sent command "Help catalog link"': 'help_catalog_link',
        'Sent command "Info"': 'help_info',
        'Sent command "Feedback"': 'help_feedback',
        'Sent command "No limits"': 'help_no_limits',
        'Sent unknown command': 'help_command_not_found',
        'Sent command "WB analyse item"': 'wb_analyse_item',
        'Sent not supported marketplace command': 'help_marketplace_not_supported',
        'Sent command on maintenance mode': 'help_maintenance_mode',
    }

    if name in slug_list.keys():
        log_item = Command.objects.create(
            user=user,
            command=slug_list[name],
            message=text,
        )
    else:
        logger.error('Command %s not in slug list, it must me updated', name)

        return None

    process_event(name, user)

    return log_item


def help_start(update: Update, context: CallbackContext):
    user = user_get_by_update(update)

    process_command(name='Started bot', user=user)

    context.bot.send_message(
        chat_id=user.chat_id,
        text=f'Приветствую, {user.full_name}!\n\nЗадача бота – помочь тебе разобраться в своих товарах и отзывах на них. Выберите один из демо-отчетов чтобы оченить работу бота:',
        reply_markup=select_report_markup,
    )


def help_info(update: Update, context: CallbackContext):
    user = user_get_by_update(update)

    process_command(name='Sent command "Info"', user=user)

    context.bot.send_message(
        chat_id=user.chat_id,
        text='📊 Этот телеграм бот поможет собирать данные отзывов на товары на Wildberries и анализировать их. Выберите один из демо-отчетов чтобы оченить работу бота:',
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton('Отчет по товару 1', callback_data='keyboard_report_1')],
            [InlineKeyboardButton('Отчет по товару 2', callback_data='keyboard_report_2')],
            [InlineKeyboardButton('Отчет по товару 3', callback_data='keyboard_report_3')],
            [InlineKeyboardButton('Отчет по товару 4', callback_data='keyboard_report_4')],
        ]),
    )


def help_command_not_found(update: Update, context: CallbackContext):
    user = user_get_by_update(update)
    process_command(name='Sent unknown command', user=user, text=update.message.text)

    context.bot.send_message(
        chat_id=user.chat_id,
        text='⚠️🤷 Непонятная команда.\nСкорее всего, вы указали неправильную команду. Сейчас бот может анализировать только ссылки на демонстрационные товары.',
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton('💁‍️ Как правильно указать категорию?', callback_data='keyboard_help_catalog_link')],
        ]),
    )


def help_maintenance_mode(update: Update, context: CallbackContext):
    user = user_get_by_update(update)
    process_command(name='Sent command on maintenance mode', user=user, text=update.message.text)

    context.bot.send_message(
        chat_id=user.chat_id,
        text='🧩 Наш сервис обновляется. Мы обновляем сервис и не можем обработать ваш запрос. Как только обновление будет готово мы сразу же оповестим вас.',
    )


def report_1(update: Update, context: CallbackContext):
    user = user_get_by_update(update)

    report_file = generate_report(username=user.full_name)

    context.bot.send_document(
        chat_id=user.chat_id,
        document=report_file,
        caption='Отчет по товару 1',
        filename='report_1.pdf',
    )


def report_2(update: Update, context: CallbackContext):
    user = user_get_by_update(update)

    report_file = generate_report(username=user.full_name)

    context.bot.send_document(
        chat_id=user.chat_id,
        document=report_file,
        caption='Отчет по товару 2',
        filename='report_2.pdf',
    )


def report_3(update: Update, context: CallbackContext):
    user = user_get_by_update(update)

    report_file = generate_report(username=user.full_name)

    context.bot.send_document(
        chat_id=user.chat_id,
        document=report_file,
        caption='Отчет по товару 3',
        filename='report_3.pdf',
    )


def report_4(update: Update, context: CallbackContext):
    user = user_get_by_update(update)

    report_file = generate_report(username=user.full_name)

    context.bot.send_document(
        chat_id=user.chat_id,
        document=report_file,
        caption='Отчет по товару 4',
        filename='report_4.pdf',
    )


def reset_webhook(bot, url, token):
    bot.delete_webhook()
    bot.set_webhook(url=url + token)


def start_bot(bot):
    dp = Dispatcher(bot, None, workers=0, use_context=True)

    dp.add_handler(CommandHandler('start', help_start))
    dp.add_handler(CommandHandler('help', help_start))

    dp.add_handler(MessageHandler(Filters.text & Filters.regex('ℹ️ О сервисе'), help_info))

    dp.add_handler(CallbackQueryHandler(report_1, pattern='keyboard_report_1'))
    dp.add_handler(CallbackQueryHandler(report_2, pattern='keyboard_report_2'))
    dp.add_handler(CallbackQueryHandler(report_3, pattern='keyboard_report_3'))
    dp.add_handler(CallbackQueryHandler(report_4, pattern='keyboard_report_4'))


    dp.add_handler(MessageHandler(Filters.all, help_info))

    return dp
