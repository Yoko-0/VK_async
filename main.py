import asyncio
from async_vk import Async_vk



async def main():
    token = '927d0c2eb68bc3197ee29a3634b0de4466b1b66ec0cddbc76142138a1e1c8dc83f2b35fb8354e013c3a25'
    group_id = 195205545
    vk_api = Async_vk(token)
    longpool = await vk_api.update_bot_longpool(group_id)

    async for msg in vk_api.listen():
        vk_api.dispatch(msg)





    #await vk_api.send_msg(peer_id = 146389567, msg = 'дадова')


asyncio.run(main())
