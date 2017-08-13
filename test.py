import time
from selenium import webdriver


SCROLL_SCRIPT = 'window.scrollTo(0, document.body.scrollHeight);'
DELAY = 0.1
MAX_NO_CHANGES = 10


driver = webdriver.PhantomJS()
driver.get('https://vk.com/geomslayer')

prev_len = len(driver.page_source)
no_changes = 0

while no_changes < MAX_NO_CHANGES:
    driver.execute_script(SCROLL_SCRIPT)
    time.sleep(DELAY)
    if prev_len < len(driver.page_source):
        prev_len = len(driver.page_source)
        no_changes = 0
        print('changed')
    else:
        print('no changes')
        no_changes += 1

posts = driver.find_elements_by_class_name('post_info')
print(len(posts), posts)
