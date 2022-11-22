import random
import string
from datetime import datetime
from time import time
import threading




class SafeWriter:
    def __init__(self, file):
        self.file = file
        self.lock = threading.Lock()

    def write(self, data):
        self.lock.acquire()
        filewriter = open(self.file, "a")
        filewriter.write(data)
        filewriter.close()
        self.lock.release()



def get_random_element(data):
    return random.choice(data)


def generate_random_string(N):
    return ''.join(random.choice(string.ascii_lowercase) for _ in range(N))


def get_readable_timestamp():
    time_st = datetime.fromtimestamp(time()).strftime('%Y-%m-%d %H:%M:%S')
    return time_st