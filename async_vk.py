import aiohttp
import asyncio
import json
from random import randint
from threading import Thread

def get_random_id():
    return randint(1, 10000000)

class Msg:
    def __init__(self, event):
        self.user_id = event['from_id']
        self.text = event['text']


class Async_vk:
    def __init__(self, token, version = 5.131):
        self.token = token
        self.base_url = 'https://api.vk.com/method/'
        self.version = version
        self.wait = 25
        self.key = None
        self.server = None
        self.ts = None
        self.events = []
        self.listeners = []
        self.loop = asyncio.get_event_loop()


    async def method(self, method_name, args):
        base_url = self.base_url + method_name
        params = {'access_token': self.token, 'v': self.version, **args}

        async with aiohttp.ClientSession() as session:
            async with session.post(base_url, data = params) as resp:
                response = await resp.json()

                if 'error' in response.keys():
                    print(f'Error in method {method_name} with error code {response["error"]["error_code"]}\nFull response {response}')
                    raise Exception

                return response['response']


    async def send_msg(self, peer_id, msg, keyboard = None):
        base_url = self.base_url + 'messages.send'
        params = {'access_token': self.token,
                    'v': self.version,
                    'user_id': peer_id,
                    'message': msg,
                    'random_id': get_random_id(),}
        if keyboard:
            params['keyboard'] = keyboard

        async with aiohttp.ClientSession() as session:
            async with session.post(base_url, data=params) as resp:
                print(await resp.json())

    async def update_bot_longpool(self, group_id, update_ts=True):
        longpool = await self.method('groups.getLongPollServer', {'group_id': group_id})
        self.key = longpool['key']
        self.server = longpool['server']

        if update_ts:
            self.ts = longpool['ts']


    async def check(self):
        """ Получить события от сервера один раз """

        values = {
            'act': 'a_check',
            'key': self.key,
            'ts': self.ts,
            'wait': self.wait,
        }

        async with aiohttp.ClientSession() as session:
            async with session.post(self.server, params = values, timeout=self.wait + 10) as resp:
                response = await resp.json()
                if 'failed' not in response:
                    self.ts = response['ts']
                    #{'user1' : ['event1', 'event2']}
                    new_events = [raw_event for raw_event in response['updates']]
                    new_events = filter(lambda event: event['type'] == 'message_new', new_events)
                    new_events = list(map(lambda event: Msg(event['object']['message']), new_events))
                    self.events += new_events

                elif response['failed'] == 1:
                    self.ts = response['ts']

                elif response['failed'] == 2:
                    self.update_bot_longpool(update_ts=False)

                elif response['failed'] == 3:
                    self.update_bot_longpool()

        return []


    async def listen(self):
        """ Слушать сервер """

        while True:
            await self.check()
            for msg in self.events:
                yield msg
                self.events.remove(msg)



    async def wait_for(self, msg, check, timeout = 60):

        future = self.loop.create_future()
        self.listeners.append((future, check))
        print(self.listeners)
        return await asyncio.wait_for(future, timeout)
        # self.waiting_users.remove(msg.user_id)
        #
        # return result



    def dispatch(self, msg):
        # dispatch new event for listeners if has
        for listener in self.listeners:
            if listener[1](msg):
                listener[0].set_result(msg)
                self.listeners.remove(listener)
                return

        # else if no listeners
        task = asyncio.create_task(self.on_message(msg))


    async def on_message(self, msg):
        if msg.text == 'kek':
            user_id = msg.user_id

            def check(msg):
                return msg.user_id == user_id and msg.text == 'lol'

            await self.send_msg(msg.user_id, 'Жду лола')
            msg = await self.wait_for(msg, check)
            print(msg)
            await self.send_msg(msg.user_id, 'HI')

        if msg.text == 'asd':
            await self.send_msg(msg.user_id, 'hue')
