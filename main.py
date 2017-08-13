import requests
from vk_login import VKAuth

APP_ID = '6087891'
PERMISSIONS = ['friends']
API_VERSION = '5.67'

auth_object = VKAuth(PERMISSIONS, APP_ID, API_VERSION)
auth_object.auth()
# r = requests.get('https://api.vk.com/method/friends.get',
#                  params={'access_token': auth_object.get_token(), 'v': API_VERSION})
# print(r.json())

lisa = auth_object.session.get('https://vk.com/audios297976573')
print(lisa.text)
