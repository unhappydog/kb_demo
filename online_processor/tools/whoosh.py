from whoosh.index import create_in, open_dir
from whoosh.fields import *
from whoosh.qparser import QueryParser
from settings import BASE_DIR
import os


class whooshIndex:
    def __init__(self, path):
        self.path = path
        self.schema = Schema(title=Text(stored=True), path=ID(stored=True), content=Text)
        if not os.path.exists(self.path):
            os.mkdir(self.path)
            self.ix = create_in(self.path, self.schema)
        else:
            self.ix = open_dir(self.path)

    def add_doc(self, doc):
        writer = self.ix.writer()
        writer.add_document(**doc)
        writer.commit()

    def query(column, value):
        with self.ix.searcher() as searcher:
            query = QueryParser(column, self.ix.schema).parse(value)
            result = searcher.search(query)
            return result
