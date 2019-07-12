from scripts import push_datas
from scripts import syn_news as sn
import click

@click.command()
@click.option("--push_data", default=True, help="push datas, need data_type")
@click.option("--data_type", default="news", help="which datatype to push:news, talent, cv, company, baidubaipin")
@click.option("--syn_news", default=False, help="syn news")
@click.option("--syn_weixin", default=False, help="syn weixins")
@click.option("--syn_major", default=False, help="syn majors")
def _main(push_data, data_type, syn_news, syn_weixin, syn_major):
    if push_data:
        push_datas.push(data_type)
    elif syn_news:
        sn.syn_new()
    elif syn_weixin:
        sn.syn_weixin()
    elif syn_major:
        sn.syn_major()

if __name__ == '__main__':
    _main()
