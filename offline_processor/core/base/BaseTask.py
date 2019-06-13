from abc import ABCMeta, abstractmethod


class BaseTask:
    __metaclass__ = ABCMeta

    def __init__(self):
        self.data = None

    @abstractmethod
    def fit(self, data):
        return data