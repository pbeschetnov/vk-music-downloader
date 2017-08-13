from selenium_vk import VKDownloader


vk = VKDownloader(email_phone='geomslayer@gmail.com', password='qqqqqq1')
vk.login()
vk.get_friends()
vk.fetch_friends_music()
