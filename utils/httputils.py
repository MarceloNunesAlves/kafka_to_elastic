import base64

'''
    Criação de chave no Elastic
    POST /_security/api_key
    {
      "name": "my-api-key"
    }

    key = {
        "id": "XXXXXXXXXXXXXXXXXXXX",
        "name": "my-api-key",
        "api_key": "YYYYYYYYYYYYYYYYY"
    }
'''

def setHeaders(contextType):

    headers = {
        "Content-type": contextType,
        "Accept": "application/json"
    }

    return headers