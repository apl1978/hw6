import api
import requests


class YaUploader:
    def __init__(self, token: str):
        self.token = token

    def upload(self, file_path: str):
        url = 'https://cloud-api.yandex.net/v1/disk/resources/upload'
        dict_header = {'Accept': 'application/json', 'Authorization': f'OAuth {token}'}
        dict_params = {"path": file_path, "overwrite": "true"}
        resp = requests.get(url, headers=dict_header, params=dict_params)
        resp.raise_for_status()
        href = resp.json().get('href')
        resp = requests.put(href, data=open(file_path, 'rb'))
        resp.raise_for_status()
        if resp.status_code == '201':
            print('Success')


if __name__ == '__main__':
    path_to_file = 'test.txt'
    token = api.token
    uploader = YaUploader(token)
    result = uploader.upload(path_to_file)
