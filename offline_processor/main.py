# from core.executor import baseExecutor
from core.ProcessorManage import ProcessorManager, DataSources
from core.MainLoop import main_loop
import click

@click.command()
@click.option("--start", default=True, help='if start queu')
@click.option("--workers", default=4, help="how many processors to start up")
def _main(start, workers):
    if start:
        main_loop(workers)

if __name__ == '__main__':
    _main()
