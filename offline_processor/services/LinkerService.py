from core.common.TerminologyLinker import TerminologyLinker
from utils.Tags import Singleton


@Singleton
class LinkerService:
    def __init__(self):
        self.linker = TerminologyLinker()

    def link_terminology(self, word_list, language):
        return self.linker.recongnize_termnology(word_list, language)

linkService = LinkerService()