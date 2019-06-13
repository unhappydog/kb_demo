from rest_apps import create_app
import settings
from services.CVService import CVService
import os
# app = create_app()

# if __name__ == '__main__':
#     app.run(host=settings.host, port=settings.port)
if __name__=='__main__':
    cv_service = CVService()
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    getdir = [files[2] for files in os.walk('/tmp/pycharm_141/resources/static/uploads/')][0]
    # # f_path = os.path.join(BASE_DIR, 'resources', 'static', 'uploads', '智联招聘_韩先生_中文_20190415_1555295482821.doc')
    # # f.save(f_path)
    for line in getdir:
        data = cv_service.parse_from_local('/tmp/pycharm_141/resources/static/uploads/'+line)