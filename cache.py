import threading
import random


class EntityCache:
    def __init__(self):
        self.lock = threading.Lock()
        self.data_dict = {}
        self.count_insert = 0

    
    def increase_one_insert(self):
        self.lock.acquire()
        self.count_insert +=1
        self.lock.release()

    
    def get_count_insert(self):
        self.lock.acquire()
        val = self.count_insert
        self.lock.release()
        return val

    
    def add_entity(self, id):
        self.lock.acquire()
        self.data_dict[id] = 0
        self.lock.release()

    
    def pick_random_entity(self,):
        self.lock.acquire()
        length = len(self.data_dict.keys())
        if length == 0:
            self.lock.release()
            return None
        value = list(self.data_dict.keys())[random.randint(0, length - 1)]
        self.lock.release()
        return value
