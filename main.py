
from async_vk_lib.async_vk import Async_vk
import asyncio
import os


token = '927d0c2eb68bc3197ee29a3634b0de4466b1b66ec0cddbc76142138a1e1c8dc83f2b35fb8354e013c3a25'
group_id = 195205545
bot = Async_vk(token)

for dir in os.listdir('./cogs'):
    if 'index.py' in os.listdir(f'./cogs/{dir}'):
        bot.load_extension(f'cogs.{dir}.index')

@bot.command(name = 'test')
async def test(ctx):
    await ctx.bot.send(ctx.message.user_id, 'Дадова ебать, жду от тебя хуй')
    user_id = ctx.message.user_id

    def check(ctx):
        return user_id == ctx.message.user_id and ctx.message.text == 'хуй'

    try:
        ctx = await ctx.bot.wait_for(check, timeout = 10)
        await ctx.bot.send(ctx.message.user_id, 'получил хуй')

    except asyncio.TimeoutError:
        await ctx.bot.send(ctx.message.user_id, 'не дождался хуя')


@bot.command(name = 'print')
async def test_print(ctx):
    print('print print')

@bot.command(name = 'hello')
async def test_hello(ctx):
    print(ctx)


bot.run_bot(group_id)
