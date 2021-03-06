from utils.Logger import logging

import time


class BaseProcessor(object):
    def __init__(self):
        self.processors = []
        self.preprocessors = []
        self.afterprocessors = []

    def add_as_processors(self, order=0, stage=1, *args, **kwargs):
        def wrapper(cls):
            self.processors.append((cls(*args, **kwargs), order, stage))

        return wrapper

    def start_process(self, datas):
        self.processors.sort(key=lambda x: x[1])
        processors = self.processors
        logging.info("there is {0} processors to be executed".format(len(processors)))
        count = 0
        for processor in processors:
            logging.info("executing processors {0}".format(processor))
            start_time = time.time()
            datas = processor[0].fit(datas)
            end_time = time.time()
            count += 1
            logging.info("processor {0} cost time {1}".format(count, end_time - start_time))
        print(len(datas))
        return datas

    def update_result(self, df, controller, key_column="_id"):
        controller.update_datas_from_df(df, key_column)

    def save_result(self, df, controller):
        controller.insert_datas_from_df(df)

    def save_result_to_processed(self, df, controller, key_column="_id"):
        controller.insert_datas_from_df(df,key_column,True)
