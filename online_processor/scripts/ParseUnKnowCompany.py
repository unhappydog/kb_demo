from services.LinkerService import linkerService
from services.KgizeService import kgService
from data_access.controller.KbTalentBankController4Mongo import KBTalentBankController4Mongo
from services.tool_services.MongoService import mgService

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
    with open(os.path.join(BASE_DIR, 'resources', 'misCompanys.txt'), 'r+', encoding='utf8') as f:
        line = f.readline()
        while line:
            result.add(line)
            line = f.readline()
    with open(os.path.join(BASE_DIR, 'resources', 'misCs'), 'w', encoding='utf8') as f:
        for line in list(result):
            f.write(line)
    print(len(result))


if __name__ == '__main__':
    # parse_one()
    remove_dual()