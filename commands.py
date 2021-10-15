

class Bot:
    def __init__(self):
        self.commands = []


    def command(self, name):
        def decorator(fn):
            new_command = {
                'execute': fn,
                'name': name
            }
            def wrapper(event):
                fn(event)

            self.commands.append(new_command)
            return wrapper
        return decorator





bot = Bot()


@bot.command(name = 'test111')
def test():
    print('random print')

@bot.command(name = 'print')
def test_print():
    print('print print')

@bot.command(name = 'hello')
def test_hello(event):
    print(event)


message = 'hello sdkfmlsd'
event = 'event'
for command in bot.commands:
    if message.startswith(command['name']):
        command['execute'](event)
