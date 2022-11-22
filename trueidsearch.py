from const import INDEX_URL, UPDATE_STATUS_URL, SEARCH_URL, CREATE_DB



def index_face(client, collection, image, request_id, user_id, is_selfie=True):
    body = {
        'base64_image_data': image,
        'search_db': collection,
        'skip_check_exist': False,
        'run_detection': True,
        'embedding_model': 'arcface',
        'request_id': request_id,
        'user_id': user_id,
        'image_id': 'test_milvus_crash_image'
    }
    url = INDEX_URL.format('id')
    if is_selfie:
        url = INDEX_URL.format('selfie')
    res = client.put(url, json=body)
    return res


def update_status(client, collection, request_id):
    body = {
        'search_db': collection,
    }
    url = UPDATE_STATUS_URL.format(request_id)
    res = client.put(url, json=body)
    return res


def search_face(client, collection, image, is_selfie=True):
    body = {
        'base64_image_data': image,
        'search_db': collection,
        'run_detection': True,
        'embedding_model': 'arcface',
        'image_id': 'test_milvus_crash_search_image'
    }
    url = SEARCH_URL.format('id')
    if is_selfie:
        url = SEARCH_URL.format('selfie')

    res = client.post(url, json=body)
    return res


def create_db(client, name):
    body = {
        "db_name": name,
        "version": "1.0"
    }
    res = client.post(CREATE_DB, json=body)
    return res
