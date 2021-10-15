
from async_vk_lib.async_vk import Async_vk



token = '927d0c2eb68bc3197ee29a3634b0de4466b1b66ec0cddbc76142138a1e1c8dc83f2b35fb8354e013c3a25'
group_id = 195205545
bot = Async_vk(token)


@bot.command(name = 'test')
async def test(ctx):
    await ctx.bot.send(ctx.message.user_id, 'Дадова ебать')

@bot.command(name = 'print')
async def test_print(ctx):
    print('print print')

@bot.command(name = 'hello')
async def test_hello(ctx):
    print(ctx)


bot.run_bot(group_id)
