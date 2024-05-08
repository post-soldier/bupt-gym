import json
import os
import random
import re
import time
import urllib.request

import ddddocr
import requests
from selenium import webdriver
from selenium.common import WebDriverException
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By

with open("../PHPSESSID.txt", "r") as f1:
    PHPSESSID = f1.read()


def slider():
    ua = "TW96aWxsYS81LjAgKFdpbmRvd3MgTlQgMTAuMDsgV2luNjQ7IHg2NCkgQXBwbGVXZWJLaXQvNTM3LjM2IChLSFRNTCwgbGlrZSBHZWNrbykgQ2hyb21lLzEyMy4wLjAuMCBTYWZhcmkvNTM3LjM2="
    cookies = {
        'PHPSESSID': PHPSESSID,
    }
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        "Accept-Encoding": "gzip, deflate, br, zstd",
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Cache-Control': 'no-cache',
        'Connection': 'keep-alive',
        'Pragma': 'no-cache',
        'Referer': 'https://reservation.bupt.edu.cn/',
        'Sec-Fetch-Dest': 'script',
        'Sec-Fetch-Mode': 'document',
        'Sec-Fetch-Site': 'none',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36 NetType/WIFI MicroMessenger/7.0.20.1781(0x6700143B) WindowsWechat(0x6309092b) XWEB/9079 Flue',
        'sec-ch-ua': '"Google Chrome";v="123", "Not:A-Brand";v="8", "Chromium";v="123"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Android"',
        'upgrade-insecure-requests': '1',
    }
    subid = int(random.random()*10)+1
    params = {
        'aid': '2015845977',
        'protocol': 'https',
        'accver': '1',
        'showtype': 'popup',
        'ua': ua,
        'noheader': '1',
        'fb': '1',
        'aged': '0',
        'enableAged': '0',
        'enableDarkMode': '0',
        'grayscale': '1',
        'clientype': '2',
        'cap_cd': '',
        'uid': '',
        'lang': 'zh-cn',
        'entry_url': 'https://reservation.bupt.edu.cn/index.php/Wechat/Booking/confirm_booking',
        'elder_captcha': '0',
        'js': '/tcaptcha-frame.fdf8b4d5.js',
        'login_appid': '',
        'wb': '1',
        'subsid': subid,
        'sess': '',
        "callback": '_aq_' + str(int(random.random() * 1e6))
    }

    response = requests.get('https://turing.captcha.qcloud.com/cap_union_prehandle', params=params, cookies=cookies,
                            headers=headers)
    j = json.loads(re.findall("\{.*?}", response.text)[0])

    sess = j["sess"]
    sid = j["sid"]

    caps = {
        "browserName": "chrome",
        'goog:loggingPrefs': {'performance': 'ALL'}  # 开启日志性能监听
    }
    opinion = webdriver.ChromeOptions()
    for key, value in caps.items():
        opinion.set_capability(key, value)

    opinion.add_argument(
        "User-Agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36 NetType/WIFI MicroMessenger/7.0.20.1781(0x6700143B) WindowsWechat(0x6309092b) XWEB/9079 Flue")

    opinion.add_argument("cookie=PHPSESSID="+PHPSESSID)
    service = webdriver.ChromeService(executable_path='../venv/Scripts/chromedriver.exe')
    driver = webdriver.Chrome(service=service, options=opinion)

    target_url = f"https://turing.captcha.qcloud.com/cap_union_new_show?aid=2015845977&protocol=https&accver=1" \
                 f"&showtype=popup&ua={ua}&noheader=1&fb=1&aged=0&enableAged=0&enableDarkMode=0&grayscale=1&clie" \
                 f"ntype=2&sess={sess}&fwidth=0&sid={sid}&wxLang=&tcScale=1&uid=&cap_cd=&rnd=" \
                 f"{int(random.random() * 1e6)}&prehandleLoadTime=" \
                 f"{int(random.random() * 100 + 100)}&createIframeStart={int(time.time())}&global=0&subsid={subid+1}"
    driver.get("https://www.baidu.com")
    driver.set_window_size(480, 600)  # 页面大小
    driver.add_cookie({"name": "PHPSESSID", "value": PHPSESSID})
    driver.get(target_url)

    button = driver.find_element(By.ID, "tcaptcha_drag_thumb")
    slide_block = driver.find_element(By.ID, "slideBlock")
    slideBg = driver.find_element(By.ID, "slideBg")
    slide_block_url = slide_block.get_attribute("src")
    slideBg_url = slideBg.get_attribute("src")

    if not os.path.exists("images"):
        os.makedirs("images")

    urllib.request.urlretrieve(slide_block_url, "images/slideBlock.png")
    urllib.request.urlretrieve(slideBg_url, "images/slideBg.png")

    slide = ddddocr.DdddOcr(det=False, ocr=False, show_ad=False)
    with open("images/slideBg.png", "rb") as f:
        Bg = f.read()

    with open("images/slideBlock.png", "rb") as f:
        slice = f.read()

    result = slide.slide_match(slice, Bg, simple_target=True)
    distance = result["target"][0] - 160


    tracks = []

    for i in range(5):
        tracks.append(distance / 5)



    action = ActionChains(driver, duration=100)  # 100ms移动一次
    action.click_and_hold(button).perform()

    for i in tracks:
        action.move_by_offset(xoffset=i, yoffset=0).perform()

    # action.drag_and_drop_by_offset(button,distance,0)

    action.release().perform()

    while driver.find_element(By.ID, "statusSuccess").text is None:
        pass

    time.sleep(2)  # 等待数据请求

    performance_log = driver.get_log('performance')  # 获取名称为 performance 的日志
    for packet in performance_log:
        message = json.loads(packet.get('message')).get('message')  # 获取message的数据
        if message.get('method') != 'Network.responseReceived':  # 如果method 不是 responseReceived 类型就不往下执行
            continue
        requestId = message.get('params').get('requestId')  # 唯一的请求标识符。相当于该请求的身份证
        url = message.get('params').get('response').get('url')  # 获取 该请求  url
        if "cap_union_new_verify" in url:
            try:
                resp = driver.execute_cdp_cmd('Network.getResponseBody', {'requestId': requestId})  # selenium调用 cdp
                ticket = json.loads(resp["body"])["ticket"]
                code = json.loads(resp["body"])["errorCode"]
            except WebDriverException:  # 忽略异常
                pass

    driver.close()
    if code == '12':
        print("wait for a minute")
        return None
    elif code != '0':
        print(code)
        return slider()
    else:
        print(resp)
        return ticket


t = slider()
with open("ticket.txt", "w") as f:
    f.write(t)
