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
        self.user_events = {}
        self.waiting_users = []
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
                    user_events = [raw_event for raw_event in response['updates']]
                    for event in user_events:
                        if event['type'] == 'message_new':
                            user_id = event['object']['message']['from_id']

                            if user_id in self.user_events.keys():
                                self.user_events[user_id].append(Msg(event['object']['message']))
                            else:
                                self.user_events[user_id] = [Msg(event['object']['message'])]

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
            for user in self.user_events:
                for msg in self.user_events[user]:
                    yield msg
                    if user not in self.waiting_users:
                        self.user_events[user].remove(msg)


    async def wait_for(self, msg, check, timeout = 60):
        self.waiting_users.append(msg.user_id)

        future = self.loop.create_future()
        self.listeners.append((future, check))
        print(self.listeners)
        return await asyncio.wait_for(future, timeout)
        # self.waiting_users.remove(msg.user_id)
        #
        # return result



    def dispatch(self):
        while True:
            for user in self.user_events:
                for msg in self.user_events[user]:
                    for listener in self.listeners:
                        if listener[1](msg):
                            listener[0].set_result(msg)
