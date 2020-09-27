import time
import requests
import pytesseract
from PIL import Image
from selenium.webdriver import Chrome
from selenium.webdriver.support.ui import Select

# 二值化(非黑即白)
def ocr(f):
    #  轉灰階
    img = Image.open(f).convert("L")
    img.save("gray.jpg")
    # 對每一個灰階像素(0-255)做一個黑白對應(0-1)
    threshhold, table = 120, []
    for i in range(256):
        if i < threshhold:
            table.append(0)
        else:
            table.append(1)
    # "1"(一)這是黑白模式
    img = img.point(table, "1")
    img.save("final.jpg")
    # OCR
    text = pytesseract.image_to_string(img.convert("RGB"))
    text = text.replace(" ", "")
    print("轉換過後:", text)
    return text

driver = Chrome("./chromedriver")
# driver.maximize_window()
url = "https://emask.taiwan.gov.tw/msk/index.jsp"
driver.get(url)
# BS: find, find_all
# Selenium: find_element_byxxx, find_elements_byxxxx
driver.find_element_by_id("btnSimple").click()
time.sleep(1)
driver.find_element_by_id("btnSysCheckNext").click()
time.sleep(1)

element = driver.find_element_by_id("simpleModal_taxPeriod")
Select(element).select_by_index(1)
driver.find_element_by_id("simpleModal_idn").send_keys("H123413647")
driver.find_element_by_id("simpleModal_mobile3").send_keys("819")

while True:
    # cookies: Server(名字:驗證碼) cookies包含名字
    cookies = {}
    for d in driver.get_cookies():
        cookies[d["name"]] = d["value"]
    # 送出網址: 其實伺服器的驗證碼已經換了(不要去看頁面上, 看存檔)
    element = driver.find_element_by_id("checkCode")
    imgurl = element.get_attribute("src")
    response = requests.get(imgurl,
                            cookies=cookies,
                            stream=True,
                            verify=False)
    # 自訂
    captcha = ocr(response.raw)
    #  你要清掉再打
    driver.find_element_by_id("captcha").clear()
    driver.find_element_by_id("captcha").send_keys(captcha)

    driver.find_element_by_id("btnDoLogin").click()

    time.sleep(1)
    # 你有訂購
    if "main" in driver.current_url:
        element = driver.find_element_by_class_name("box-body")
        print(element.text)
        break
    # 你沒有訂購
    else:
        element = driver.find_element_by_class_name("modal-body")
        # BS: .text  ["href"]
        # Selenium: .text   get_attribute("href")
        if "查無" in element.text:
            print("無訂購")
            break
        else:
            print("驗證碼錯誤")
            driver.find_element_by_class_name("close").click()
            # time.sleep(1)
time.sleep(1)
driver.close()