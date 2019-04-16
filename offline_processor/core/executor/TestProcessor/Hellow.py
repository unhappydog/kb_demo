from core.executor import baseExecutor

@baseExecutor.add_as_processor(order=1)
def execute(test=""):
    print(test)
    print('hellow')
