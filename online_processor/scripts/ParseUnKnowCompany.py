import sys
sys.path.append(".")
from services.LinkerService import linkerService
from services.KgizeService import kgService
from data_access.controller.KbTalentBankController4Mongo import KBTalentBankController4Mongo
from services.tool_services.MongoService import mgService
import click

def parse_one():
    controller = KBTalentBankController4Mongo()
    cvs = controller.get_datas()
    for cv in cvs:
        try:
            cv = linkerService.parse(cv)
            linkerService.link_company(cv)
        except Exception as e:
            # print("_____________________",cv['_id'])
            mgService.delete({'_id':cv['_id']},'kb_demo', 'kb_talent_bank')

def remove_dual():
    from settings import BASE_DIR
    import os
    result = set()
    with open(os.path.join(BASE_DIR, 'resources', 'company.txt'), 'r+', encoding='utf8') as f:
        line = f.readline()
        while line:
            result.add(line)
            line = f.readline()
    with open(os.path.join(BASE_DIR, 'resources', 'uncompany.txt'), 'w', encoding='utf8') as f:
        for line in list(result):
            f.write(line)
    print(len(result))

@click.command()
@click.option('--parse', default=1, help='1 for parse, 2 for remve dual')
def _main(parse):
    if parse == 1:
        parse_one()
    elif parse == 2:
        remove_dual()
    else:
        print("unknown command")


if __name__ == '__main__':
    _main()
    # parse_one()
    # remove_dual()
