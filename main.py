
from async_vk import Async_vk



token = '927d0c2eb68bc3197ee29a3634b0de4466b1b66ec0cddbc76142138a1e1c8dc83f2b35fb8354e013c3a25'
group_id = 195205545
vk_api = Async_vk(token)
vk_api.run_bot(group_id)
