import aioschedule as schedule
import asyncio
from bot_8 import *

async def scheduler():
    schedule.every().seconds.do(send_reminder)
    while True:
        await asyncio.sleep(1)
        await schedule.run_pending()