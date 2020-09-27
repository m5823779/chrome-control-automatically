import time
from selenium.webdriver import Chrome

url = "https://facebook.com"
driver = Chrome("./chromedriver")
driver.get(url)

# bs: find/find_all
# selenium: find_element/find_elements
# clear: 清除裡面原有字串 # send_keys: 輸入字串
driver.find_element_by_id("email").send_keys("123456@gmail.com")
driver.find_element_by_id("pass").send_keys("123456")
# click: 點擊
time.sleep(1)
driver.find_element_by_id("u_0_b").click()