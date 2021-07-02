from elasticsearch import Elasticsearch
from utils import httputils
import http.client
import os

'''
    Exemplo de envio
    {
        "measurement": "brushEvents",
        "tags": {
            "user": "Carol",
            "brushId": "6c89f539-71c6-490d-a28d-6c5d84c0ee2f"
        },
        "time": "2018-03-28T8:01:00Z",
        "fields": {
            "duration": 127
        }
    }
'''

url = os.environ.get('URL_ELK', 'localhost:9200')  # export URL_ELK=localhost:9200
user = os.environ.get('USER_ELK')  # export USER_ELK=None
senha = os.environ.get('PWD_ELK')

class ManagerElastic():

    def __init__(self):
        self.es = None
        if(user and senha):
            self.es = Elasticsearch(['https://'+ url], http_auth=(user, senha))
        else:
            self.es = Elasticsearch(['http://' + url])

    def sendData(self, index, envio):
        try:
            res = self.es.index(index=index, body=envio)
        except Exception as e:
            print('Erro na inserção. {}'.format(str(e)))

    def sendBulkElastic(self, envio):
        params = envio
        headers = httputils.setHeaders("application/x-ndjson")

        conn = None
        if (user and senha):
            conn = http.client.HTTPSConnection(url)
        else:
            conn = http.client.HTTPConnection(url)

        conn.request("POST", "/_bulk", params, headers)

        response = conn.getresponse()

        print('Status do Elasticsearch -> ' + str(response.status) + ' - ' + response.reason)

        conn.close()