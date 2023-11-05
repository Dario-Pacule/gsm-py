import requests

def post(phone, message):
    url = 'http://localhost:3000/system_gate_way'
    data = {'phoneNumber': phone, 'content': message}

    token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpYXQiOjE2OTMwMjYxMzYsImV4cCI6MTAzMzI5Mzk3MzYsInN1YiI6ImQ2MTY4ODk3LWI1MGMtNGE5Yy04ZTg3LWZmYjNlMmY1ZTBmNSJ9.1a9lMAmQjIEoVWUkAnNa46K-aJbSSmLbiFjfdjPlcoQ'

    headers = {'Authorization': f'Bearer {token}'}

    response = requests.post(url, data=data, headers=headers)

    if response.status_code == 200:
    # A requisição foi bem-sucedida
      print("Sucesso: ",response.json())
    else:
      print(f'A requisição falhou com o código de status {response.json()}')