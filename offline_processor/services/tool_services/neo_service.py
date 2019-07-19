import settings
from py2neo import Graph, Node
from utils.Tags import Singleton
from threading import Lock
from datetime import datetime
from pandas._libs.tslibs.timestamps import Timestamp
from bson import ObjectId
import numpy as np
import math


class NeoService():
    _instance = None
    _lock = Lock()

    @classmethod
    def instance(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = cls()
        return cls._instance

    def __init__(self, host=settings.neo_host, port=settings.neo_port):
        self.host = host
        self.port = port
        self.graph = None
        self.lock = Lock()
        self.connectDB()

    def connectDB(self):
        if self.graph is None:
            with self.lock:
                if self.graph is None:
                    self.graph = Graph("http://{0}:{1}".format(self.host, self.port), username="", password="")

    def exec(self, sql):
        return self.graph.run(sql)

    def update(self, label, **keywords):
        for k,v in keywords.items():
            if v is None:
                keywords[k] = ""
            if type(v) == np.float64:
                if np.isnan(v):
                    keywords[k] = ""

            if type(v) == float:
                if math.isnan(v):
                    keywords[k] = ""
            if type(v) == ObjectId:
                keywords[k] = str(v)
            elif type(v) == datetime:
                keywords[k] = v.strftime('%Y-%m-%d %H:%M:%S')
            elif type(v) == Timestamp:
                keywords[k] = v.strftime('%Y-%m-%d %H:%M:%S')

        node = Node(label, **keywords)
        try:
            self.graph.push(node)
        except Exception as e:
            print(e)

    def create(self, label, **keywords):
        for k,v in keywords.items():
            if v is None:
                keywords[k] = ""
            if type(v) == np.float64:
                if np.isnan(v):
                    keywords[k] = ""

            if type(v) == float:
                if math.isnan(v):
                    keywords[k] = ""
            if type(v) == ObjectId:
                keywords[k] = str(v)
            elif type(v) == datetime:
                keywords[k] = v.strftime('%Y-%m-%d %H:%M:%S')
            elif type(v) == Timestamp:
                keywords[k] = v.strftime('%Y-%m-%d %H:%M:%S')

        node = Node(label, **keywords)
        try:
            self.graph.create(node)
        except Exception as e:
            print(e)
            print(keywords)


