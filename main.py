<<<<<<< HEAD
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
=======
from aiogram.filters.command import Command
from aiogram import F
import requests
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.types import Message
from aiogram.utils.keyboard import  ReplyKeyboardBuilder
from data import SERVER_IPS, ADMIN_ID

dp = Dispatcher()



@dp.message(Command("start"))
async def cmd_name(message: types.Message) -> None:

    if str(message.from_user.id) in str(ADMIN_ID):

        builder = ReplyKeyboardBuilder()
        builder.row(
            types.KeyboardButton(text="Проверить доступность")
        )
        await message.answer(f"Доброго времени суток, <b>{str(message.from_user.first_name)}</b>", reply_markup=builder.as_markup())
    else:
        await message.answer("У Вас нет прав доступа")




@dp.message(F.text == "Проверить доступность")
async def check_whith_HTTP(message: Message) -> None:

    unreachable = {}
    for ip, name in SERVER_IPS.items():
        htt_url = f"http://{ip}:8080"
        print(htt_url)
        try:
            r = await requests.get(htt_url, timeout=5)  # Устанавливаем таймаут для запроса
            if r.status_code != 200:
                unreachable[ip] = name
        except requests.exceptions.ConnectTimeout:
            unreachable[ip] = name

    if unreachable:
        text = "\n".join([f"Не могу достучаться до {name} ({ip})" for ip, name in unreachable.items()])
        await message.answer(text)
    else:
        text = "Все сервера доступны."
        await message.answer(text)






async def check_servers(message: Message):
    while True:
        unreachable = {}
        for ip, name in SERVER_IPS.items():
            htt_url = f"http://{ip}:8080"
            try:
                r = await requests.get(htt_url, timeout=5)  # Устанавливаем таймаут для запроса
                if r.status_code != 200:
                    unreachable[ip] = name
            except requests.exceptions.ConnectTimeout:
                unreachable[ip] = name

        if unreachable:
            text = "\n".join([f"Не могу достучаться до {name} ({ip})" for ip, name in unreachable.items()])
            await message.answer(text)
        else:
            text = "Все сервера доступны."
            await message.answer(text)


        await asyncio.sleep(1800)





async def main():
    API_TOKEN = '6547737534:AAHL0blFWnnSQaQhEYPbTbl9sUrMCck4_EE'
    bot = Bot(token=API_TOKEN, parse_mode='HTML')
    await dp.start_polling(bot)
    await check_servers()


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Exit')
>>>>>>> 5932afb (Initial commit)
