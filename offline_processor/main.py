# from core.executor import baseExecutor
from core.ProcessorManage import ProcessorManager, DataSources
from core.MainLoop import main_loop
import click

@click.command()
@click.option("--start", default=0, help='if start queu')
@click.option("--data_type", default='new', help='which data source to execute')
def _main(start, data_type):
    if start == 1:
        main_loop()
    elif data_type == 'new':
        process = ProcessorManager()
        process.execute_processor(DataSources.new, 100)
    elif data_type == 'talent':
        process = ProcessorManager()
        process.execute_processor(DataSources.talent, 100)
    elif data_type == 'weixin':
        process = ProcessorManager()
        process.execute_processor(DataSources.weixin, 100)
    elif data_type == 'all':
        process = ProcessorManager()
        process.execute_processor(DataSources.weixin, 100)
        process.execute_processor(DataSources.talent, 100)
        process.execute_processor(DataSources.new, 100)
    else:
        print("unknow type")


if __name__ == '__main__':
    _main()
