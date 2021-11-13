import logging
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, Update
from telegram.ext import CallbackContext, CallbackQueryHandler, CommandHandler, Dispatcher, Filters, MessageHandler

from app.models import Command, TelegramUser
from app.report import generate_report

# включаем логи
logger = logging.getLogger(__name__)

reply_keyboard = ReplyKeyboardMarkup([['ℹ️ О сервисе', '🚀 Увеличить лимит запросов']], resize_keyboard=True)


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
        text=f'Приветствую, {user.full_name}!\n\nЗадача бота – помочь тебе разобраться в своих товарах и отзывах на них. Отправь ссылку на страницу товара чтобы получить ЗНАНИЯ.',
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton('💁‍️ Как правильно указать ссылку на товар?', callback_data='keyboard_help_catalog_link')],
        ]),
    )


def help_analyse_category(update: Update, context: CallbackContext):
    user = user_get_by_update(update)
    process_command(name='Sent command "Help analyse category"', user=user)

    context.bot.send_message(
        chat_id=user.chat_id,
        text='📊 Анализ выбранного товара\n\nОтправьте ссылку на страницу товара Wildberries, чтобы получить сводную информацию по ней.',
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton('💁‍️ Как правильно указать категорию?', callback_data='keyboard_help_catalog_link')],
        ]),
        disable_web_page_preview=True,
    )


def help_catalog_link(update: Update, context: CallbackContext):
    user = user_get_by_update(update)
    process_command(name='Sent command "Help catalog link"', user=user)

    context.bot.send_message(
        chat_id=user.chat_id,
        text='👉️ Чтобы провести анализ категории, скопируйте из адресной строки браузера ссылку на страницу товара с сайта Wildberries.',
        disable_web_page_preview=True,
    )


def help_info(update: Update, context: CallbackContext):
    user = user_get_by_update(update)
    process_command(name='Sent command "Info"', user=user)

    context.bot.send_message(
        chat_id=user.chat_id,
        text='📊 Этот телеграм бот поможет собирать данные отзывов на товары на Wildberries и анализировать их.',
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton('💁‍️ Как правильно указать категорию?', callback_data='keyboard_help_catalog_link')],
        ]),
    )


def help_feedback(update: Update, context: CallbackContext):
    user = user_get_by_update(update)
    process_command(name='Sent command "Feedback"', user=user)

    context.bot.send_message(
        chat_id=user.chat_id,
        text='✉️ Если вам нужна помощь, напишите нам весточку на https://canb2b.ru',
    )


def help_no_limits(update: Update, context: CallbackContext):
    user = user_get_by_update(update)
    process_command(name='Sent command "No limits"', user=user)

    context.bot.send_message(
        chat_id=user.chat_id,
        text='Если вы хотите увеличить или снять лимит запросов напишите нам напишите нам в чат поддержки или на почту aloha@wondersell.ru запрос с фразой «Снимите лимит запросов».',
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton('👨‍🚀 Написать в поддержку', url='https://canb2b.ru')],
        ]),
    )


def help_command_not_found(update: Update, context: CallbackContext):
    user = user_get_by_update(update)
    process_command(name='Sent unknown command', user=user, text=update.message.text)

    context.bot.send_message(
        chat_id=user.chat_id,
        text='⚠️🤷 Непонятная команда.\nСкорее всего, вы указали неправильную команду. Сейчас бот может анализировать только ссылки на каталоги Wildberries.',
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


def wb_analyse_item(update: Update, context: CallbackContext):
    user = user_get_by_update(update)
    process_command(name='Sent command "WB analyse item"', user=user, text=update.message.text)

    if not user.can_send_more_requests():
        dt = user.next_free_catalog_request_time()
        context.bot.send_message(
            chat_id=user.chat_id,
            text=f'💫⚠️ Ваш лимит запросов закончился.\nЧтобы продолжить работу, напишите нам в чат поддержки на сайте https://canb2b.ru с запросом на снятие ограничения, либо дождитесь восстановления лимита. Это произойдет {dt.day}.{dt.month}.{dt.year} в {dt.hour}:{dt.minute} по Лондонскому времени (UTC/GMT+0)',
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton('👨‍🚀 Написать в поддержку', url='https://canb2b.ru')],
            ]),
        )
        process_event(user=user, event='Received "Out of requests" error')

    else:
        context.bot.send_message(
            chat_id=user.chat_id,
            text='Вся магия начинается здесь',
        )

        process_event(user=user, event='Started WB item export')


def report(update: Update, context: CallbackContext):
    user = user_get_by_update(update)

    report_file = generate_report(username=user.full_name)

    context.bot.send_document(
        chat_id=user.chat_id,
        document=report_file,
        caption='Файл с отчетом',
        filename=f'report.pdf',
    )


def reset_webhook(bot, url, token):
    bot.delete_webhook()
    bot.set_webhook(url=url + token)


def start_bot(bot):
    dp = Dispatcher(bot, None, workers=0, use_context=True)

    dp.add_handler(CommandHandler('start', help_start))
    dp.add_handler(CommandHandler('help', help_start))

    dp.add_handler(MessageHandler(Filters.text & Filters.regex('ℹ️ О сервисе'), help_info))
    dp.add_handler(MessageHandler(Filters.text & Filters.regex('🚀 Увеличить лимит запросов'), help_no_limits))
    dp.add_handler(MessageHandler(Filters.text & Filters.regex('🚀 Снять ограничение'), help_no_limits))

    dp.add_handler(MessageHandler(Filters.text & Filters.regex('отчет'), report))

    dp.add_handler(CallbackQueryHandler(help_analyse_category, pattern='keyboard_analyse_category'))
    dp.add_handler(CallbackQueryHandler(help_catalog_link, pattern='keyboard_help_catalog_link'))
    dp.add_handler(CallbackQueryHandler(help_feedback, pattern='keyboard_help_info_feedback'))
    dp.add_handler(CallbackQueryHandler(help_no_limits, pattern='keyboard_help_no_limits'))

    dp.add_handler(MessageHandler(Filters.text & Filters.regex(r'www\.wildberries\.ru/catalog/.*/detail\.aspx'), wb_analyse_item))
    dp.add_handler(MessageHandler(Filters.text & Filters.regex(r'www\.wildberries\.ru/catalog/.*/search\.aspx'), help_command_not_found))
    dp.add_handler(MessageHandler(Filters.text & Filters.regex(r'www\.wildberries\.ru/brands/'), help_command_not_found))
    dp.add_handler(MessageHandler(Filters.text & Filters.regex(r'www\.wildberries\.ru/promotions/'), help_command_not_found))
    dp.add_handler(MessageHandler(Filters.text & Filters.regex(r'www\.wildberries\.ru/search\?text='), help_command_not_found))

    dp.add_handler(MessageHandler(Filters.text & Filters.regex(r'www\.wildberries\.ru/catalog/'), help_command_not_found))

    dp.add_handler(MessageHandler(Filters.all, help_command_not_found))

    return dp
