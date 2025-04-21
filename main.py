import asyncio
import os
from loguru import logger
from telethon import TelegramClient, events

from dotenv import load_dotenv
import jdatetime
from quotes import get_random_quotes
from counter import get_date_str

load_dotenv()

logger = logger.opt(colors=True)
bot = TelegramClient(session='bot', api_id=2496, api_hash='8da85b0d5bfe62527e5b244c209159c3',)

BOT_TOKEN: str = os.getenv('BOT_TOKEN')
CHANNEL: str = os.getenv('CHANNEL')
TAJROBI: str = os.getenv('TAJROBI')
ENSANI: str = os.getenv('ENSANI')
RIAZI: str = os.getenv('RIAZI')
SEND_PRE: int = int(os.getenv('SEND_PRE'))


def generate_message() -> str:
    ensani_date = jdatetime.date(*[int(x) for x in ENSANI.split(',')])
    tajrobi_date = jdatetime.date(*[int(x) for x in TAJROBI.split(',')])
    riazi_date = jdatetime.date(*[int(x) for x in RIAZI.split(',')])

    ensani_month_name = ensani_date.j_months_fa[ensani_date.month - 1]
    ensani_weekday_name = ensani_date.j_weekdays_fa[ensani_date.weekday()]

    tajrobi_month_name = tajrobi_date.j_months_fa[tajrobi_date.month - 1]
    tajrobi_weekday_name = tajrobi_date.j_weekdays_fa[tajrobi_date.weekday()]

    riazi_month_name = riazi_date.j_months_fa[riazi_date.month - 1]
    riazi_weekday_name = riazi_date.j_weekdays_fa[riazi_date.weekday()]

    earliest_date = min(ensani_date, tajrobi_date, riazi_date)
    earliest_month_name = earliest_date.j_months_fa[earliest_date.month - 1]
    
    quote: str = get_random_quotes()
    counter_str = get_date_str(earliest_date)

    message: str = f'''

    <blockquote>🎯 روز شمار نهایی کنکور {earliest_date.year} </blockquote>
    <b>🔔 لحظه‌شماری برای روز سرنوشت...</b>

    📚 کنکور {earliest_month_name} {earliest_date.year} نزدیکه!

    🗓 تاریخ برگزاری:

    🧪 تجربی: {tajrobi_weekday_name}، {tajrobi_date.day} {tajrobi_month_name}
    📖 انسانی: {ensani_weekday_name}، {ensani_date.day} {ensani_month_name}
    🔢 ریاضی: {riazi_weekday_name}، {riazi_date.day} {riazi_month_name}

    🕰 زمان باقی‌مانده تا شروع:
    <blockquote>{counter_str}</blockquote>

    🧠 یادت نره:
    <b>{quote}</b>

📌 #کنکور #کنکور_۱۴۰۴ #روز_شمار #تلاش #هدف
    '''

    return message


@bot.on(events.NewMessage(pattern='/date'))
async def event_date_message_handle(e):
    message: str = generate_message()
    await e.respond(message, parse_mode='html')



async def Worker():
    entity = await bot.get_entity(CHANNEL)
    while True:
        message: str = generate_message()
        try:
            await bot.send_message(entity, message, parse_mode='html')
            logger.success(f'Send Message to {entity.title} success...')
        
        except Exception as e:
            logger.error(f'Send Message to {entity.title} Error : {e}')
        
        await asyncio.sleep(SEND_PRE)


async def main():
    await bot.start(bot_token=BOT_TOKEN)
    info = await bot.get_me()
    logger.info(f'Conncet to @{info.username} | <c>{info.first_name}</c>')

    loop.create_task(Worker())
    await bot.run_until_disconnected()



if __name__ == '__main__':
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop=loop)
    loop.run_until_complete(main())