from telegram import Bot, Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import Filters, Updater, CommandHandler, MessageHandler, CallbackContext
from ping3 import ping
import time

API_TOKEN = ''

CAMERA_IPS = {
    '192.168.1.2': 'АЗС-01'

}
SERVER_IPS = {
    '10.11.56.9': 'ЭЗС 56'
}

users = ['', '']


def check_ips(ip_dict):
    unreachable = {}
    for ip, name in ip_dict.items():
        if not ping(ip, timeout=2):
            unreachable[ip] = name
    return unreachable


def start(update: Update, context: CallbackContext) -> None:
    user_id = update.message.chat_id
    if user_id not in users:
        users.append(user_id)

    keyboard = [
        [KeyboardButton("Проверить камеры"), KeyboardButton("Проверить сервера")]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard)
    update.message.reply_text('Выберите действие:', reply_markup=reply_markup)


def check_cameras(update: Update, _: CallbackContext) -> None:
    unreachable = check_ips(CAMERA_IPS)
    if unreachable:
        update.message.reply_text(
            "\n".join([f"Не могу достучаться до {name} ({ip})" for ip, name in unreachable.items()]))
    else:
        update.message.reply_text("Все камеры доступны.")


def check_servers(update: Update, _: CallbackContext) -> None:
    unreachable = check_ips(SERVER_IPS)
    if unreachable:
        update.message.reply_text(
            "\n".join([f"Не могу достучаться до {name} ({ip})" for ip, name in unreachable.items()]))
    else:
        update.message.reply_text("Все сервера доступны.")


def main():
    updater = Updater(token=API_TOKEN, use_context=True)

    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.regex('^Проверить камеры$'), check_cameras))
    dp.add_handler(MessageHandler(Filters.regex('^Проверить сервера$'), check_servers))

    updater.start_polling()

    while True:
        time.sleep(1800)  # 30 minutes
        cam_unreachable = check_ips(CAMERA_IPS)
        serv_unreachable = check_ips(SERVER_IPS)

        for user_id in users:
            bot = Bot(API_TOKEN)
            if cam_unreachable:
                bot.sendMessage(chat_id=user_id, text="\n".join(
                    [f"Автоматическая проверка: Не могу достучаться до {name} ({ip})" for ip, name in
                     cam_unreachable.items()]))
            if serv_unreachable:
                bot.sendMessage(chat_id=user_id, text="\n".join(
                    [f"Автоматическая проверка: Не могу достучаться до {name} ({ip})" for ip, name in
                     serv_unreachable.items()]))


if __name__ == '__main__':
    main()