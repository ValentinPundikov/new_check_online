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