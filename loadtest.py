

from dotenv import load_dotenv
from datetime import datetime
from time import time

from locust import HttpUser, between, task

from cache import EntityCache
from dataloader import ImageLoader
from trueidsearch import index_face, update_status, search_face, create_db
from utils import get_random_element, generate_random_string, get_readable_timestamp, SafeWriter

logger = SafeWriter(f"logs/trueidsearch_{get_readable_timestamp()}")

index_cache = EntityCache()
col_cache = EntityCache()

# collections = [
#     '_fc6c90d90f4fad478b8dd818ac92c900',
#     '_eaffb4b48e38d08f9f010d7bedb78879',
#     '_a50bf70f58ab9b971cc05f0e4f7cba5c',
#     '_cff1faa7295f0ae89cff96ac732b8ba8',
#     '_848e50a2d1ec34cca8849ee687edba0c',
#     '_e5a8e45601bb0759427bc6c140dddff9',
#     '_d7bc2607b6d8f97460349d81a3066b46',
#     '_5f9937bdffbef6ce15116dd1268f2c03',
#     '_584444e95b0bcfe6ae07fdf1457843c1',
#     '_d5a9bca0180f9f34df56b14ffe8dfa08',
#     '_023b126892cb968aa3f8846516f9889b',
#     '_d55d96e8506b75480a68af3e6aedcfc3',
#     '_7a535ad53c115d7cef6484aa8780c58c',
#     '_023b126892cb968aa3f8846516f9889b',
#     '_d55d96e8506b75480a68af3e6aedcfc3',
#     '_7a535ad53c115d7cef6484aa8780c58c',
#     '_396ca7aeb9f26b785267a5d632eca75e',
#     '_f8e431916e26e155eb1e1bad850522d7',
#     '_1464d0ae7b0b9d8177d1a5b84436f2a7'
# ]


def log_if_err(action, res, logger):
    time_st = datetime.fromtimestamp(time()).strftime('%Y-%m-%d %H:%M:%S')
    mess = f"{time_st} [Error]: Action = {action}, Http code = {res.status_code}, Message = {res.text}, Reason = {res.reason}"
    print(mess)
    logger.write(mess + "\n")


class TrueidSearchService(HttpUser):
    wait_time = between(1, 2)
    image_loader = ImageLoader('data/images')
    @task(10)
    def index_face(self):
        col = col_cache.pick_random_entity()
        if not col:
            return
        col = '_' + col
        image = TrueidSearchService.image_loader.get_image_base64()
        request_id = generate_random_string(16)
        user_id = generate_random_string(10)
        res = index_face(self.client, col, image, request_id, user_id, False)
        if res.status_code == 200:
            index_cache.add_entity(f'{col}:{request_id}:{user_id}')
        else:
            log_if_err(action="Index face id", res=res, logger=logger)
        
        res = index_face(self.client, col, image, request_id, user_id, True)
        if res.status_code == 200:
            index_cache.add_entity(f'{col}:{request_id}:{user_id}')
        else:
            log_if_err(action="Index face selfie", res=res, logger=logger)

    @task(5)
    def create_collection(self):
        col = generate_random_string(20)
        res = create_db(self.client, col)
        if res.status_code == 200:
            col_cache.add_entity(col)
        else:
            log_if_err(action="Create db", res=res, logger=logger)


    # @task(2)
    # def update_status(self):
    #     item = index_cache.pick_random_entity()
    #     if not item:
    #         return
    #     col, request_id, user_id = item.split(':')
    #     res = update_status(self.client, col, request_id)
    #     if res.status_code == 200:
    #         pass
    #     else:
    #         log_if_err(action="Update status", res=res, logger=logger)


    # @task(20)
    # def search_face(self):
    #     col = get_random_element(collections)
    #     image = TrueidSearchService.image_loader.get_image_base64()
    #     res = search_face(self.client, col, image, False)
    #     if res.status_code == 200:
    #         pass
    #     else:
    #         log_if_err(action="Search id face", res=res, logger=logger)
    #     res = search_face(self.client, col, image, True)
    #     if res.status_code == 200:
    #         pass
    #     else:
    #         log_if_err(action="Search selfie face", res=res, logger=logger)
