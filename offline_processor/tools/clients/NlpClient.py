import requests

class NlpClient:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.base_url = "http://{0}:{1}".format(self.host, self.port)

    def distinct(self, data):
        url = self.base_url + "/distinct"
        result = requests.post(url, data={'content':data})
        result = result.json()
        result = result['result']
        if result == 'true':
            return True
        else:
            return False
