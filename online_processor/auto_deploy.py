from fabric import Connection
import os

update_list = ['core', 'data_access', 'logs','rest_apps', 'scripts', 'services',
               'tools','unit_test','utils','main.py']
# update_list = ['Recommand.py']
# update_list = ['app']


def update():
    with Connection(host='centos1', user='root') as con:
        # con.connect_kwargs.password='1!P@ssword'
        rm_cm_format = "rm -rf {0}"
        scp_format = "scp -r {0} root@centos1:/home/lxl/online_processor/"
        rm_cm = ";".join([rm_cm_format.format("/home/lxl/online_processor/" + x) for x in update_list])
        scp_cms = [scp_format.format(x) for x in update_list]
        print(scp_cms)
        result = con.run(rm_cm)
        # result = con.run("cd /home/lxl/kjqb/Recommend/bin;bash /home/lxl/kjqb/Recommend/bin/start.sh restart")
        for scp_cm in scp_cms:
            os.system(scp_cm)
        print(result)


if __name__ == '__main__':
    update()
