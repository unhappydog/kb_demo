import settings
from py2neo import Graph, Node
from utils.Tags import Singleton
from threading import Lock


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
        self.graph.run(sql)

    def create(self, label, **keywords):
        node = Node(label, **keywords)
        self.graph.create(node)
