from .engines import *

engine_dict = {
    'reverse': ReverseEngine
}
def engine_factory(fact_type):
    return engine_dict[fact_type]()
