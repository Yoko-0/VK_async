import time

[{'type': 'message_typing_state', 'object': {'state': 'typing', 'from_id': 146389567, 'to_id': -195205545}, 'group_id': 195205545, 'event_id': '981d6094b60ddf0f1a25110a92558922dd09643a'}]
[{'type': 'message_new', 'object': {'message': {'date': 1634279312, 'from_id': 146389567, 'id': 2096, 'out': 0, 'peer_id': 146389567, 'text': 'asd', 'conversation_message_id': 1788, 'fwd_messages': [], 'important': False, 'random_id': 0, 'attachments': [], 'is_hidden': False}, 'client_info': {'button_actions': ['text', 'vkpay', 'open_app', 'location', 'open_link', 'callback', 'intent_subscribe', 'intent_unsubscribe'], 'keyboard': True, 'inline_keyboard': True, 'carousel': True, 'lang_id': 0}}, 'group_id': 195205545, 'event_id': '36ea7e2965f01a46f8715d4b955e8f1e13257a95'}]

for event in events:
    if event['type'] == 'message_new':
        user_id = event['object']['message']['from_id']
        if user_id in self.listeners.keys():
            self.listeners[user_id].append(event['object']['message'])
        else:
            self.listeners[user_id] = [event['object']['message']]
