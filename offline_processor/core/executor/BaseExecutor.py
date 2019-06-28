from utils.Tags import Singleton
import threading


class BaseExecutor(object):
    _instance_lock = threading.Lock()

    def __init__(self):
        self.processors = []
        self.after_processors = []
        self.init_processors = []

    def add_as_processor(self, order=0):
        def wrapper(cls):
            self.processors.append(cls)
        return wrapper

    def execute(self, *args, **kwargs):
        print(self)
        for p in self.processors:
            p(*args, **kwargs)
        print(self.processors)
