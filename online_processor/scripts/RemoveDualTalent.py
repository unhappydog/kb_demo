from services.tool_services.MongoService import mgService


def remove_dual():
    datas = mgService.remove_dul('id')