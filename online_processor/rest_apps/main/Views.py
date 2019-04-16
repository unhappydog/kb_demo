from . import inf_restful


@inf_restful.route(
    '/information-recommendation_test/<int:firstgrade>/<int:categoryid>/<int:uid>/<int:pageno>/<int:pagesize>/',
    methods=["GET"])
def get_article(firstgrade, categoryid, uid, pageno, pagesize):
    return "hellow world"


