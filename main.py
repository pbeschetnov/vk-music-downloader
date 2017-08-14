from selenium_vk import VKDownloader


vk = VKDownloader()
vk.login()
vk.get_friends()
vk.fetch_friends_music()
