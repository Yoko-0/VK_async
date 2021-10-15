from async_vk_lib.cog import *



class MyCog(Cog):
    def __init__(self):
        self.text = 'asdasdasd'

my_cog = MyCog()

@cog.command(name = 'asd')
async def test(ctx):
    print(my_cog.text)


def setup(bot):
    bot.add_cog(cog)
