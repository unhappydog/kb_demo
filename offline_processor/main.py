# from core.executor import baseExecutor
from core.ProcessorManage import ProcessorManager, DataSources

if __name__ == '__main__':
    process = ProcessorManager()
    # process.execute_processor(DataSources.new, 100)
    # process.execute_processor(DataSources.weixin, 100)
    # process.execute_processor(DataSources.talent, 10)
    process.multi_process_execute(DataSources.talent, 100)