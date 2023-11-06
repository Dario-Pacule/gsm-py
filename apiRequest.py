import requests

def post(phone, message):
    url = 'http://localhost:3000/system_gate_way'
    data = {'phoneNumber': phone, 'content': message}

    token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpYXQiOjE2OTMwMjYxMzYsImV4cCI6MTAzMzI5Mzk3MzYsInN1YiI6ImQ2MTY8ODk3LWI1MGMtNGE5Yy04ZTg3LWZmYjNlMmY1ZTBm5'

    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }

    try:
        response = requests.post(url, json=data, headers=headers) 

        if response.status_code == 200:
            print("Sucesso: ", response.json())
        else:
            print(f'A requisição falhou com o código de status {response.status_code}')
    except requests.exceptions.RequestException as e:
        # Lidar com erros de requisição, como timeout, conexão recusada, etc.
        print(f'Erro na requisição: {e}')
