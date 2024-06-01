import requests


def get_response(endpoint = 'http://127.0.0.1:8000/auth/login'):
    print(requests.post(endpoint,json={}).text)


get_response()