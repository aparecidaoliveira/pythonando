import requests


def get_livros():
    response = requests.get("http://127.0.0.1:8000/api/livros")

    if response.status_code == 200:
        print(response.json())
        return response.json()  # Retorna o JSON diretamente
    else:
        print(f"Erro ao obter livros: {response.status_code}")
        return {}
    # print(response.json())
    # return response.json()
