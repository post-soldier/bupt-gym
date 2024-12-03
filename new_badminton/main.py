import json
import re
import threading
import tkinter as tk
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timedelta
from tkinter import messagebox, simpledialog

import requests
import schedule

import TecentSliderVerify

lock = threading.Lock()
sign = 0

with open("./PHPSESSID.txt", "r") as f1:
    PHPSESSID = f1.read()

badminton = ["15418", "15419", "15420", "15421", "15422", "15423", "15424", "15425", "15426"]

with open('time.json', 'r', encoding='utf-8') as f:
    time_slots = json.load(f)

# 将键从字符串转换为整数
time_slots = {int(k): v for k, v in time_slots.items()}


def sendToWechat(message):
    with open("SendKey.txt", "r") as k:
        sendKey = k.read()
    print(sendKey)
    url = f"https://sctapi.ftqq.com/{sendKey}.send"
    data = {
        "title": message,
    }
    requests.post(url, data=data)


def run_schedule():
    # This function will keep checking the schedule
    schedule.run_pending()
    root.after(1000, run_schedule)  # Check every second


check_period = 15
def check_empty(area_id, date, chosen_time_period):
    job = schedule.every(check_period).seconds.do(lambda: f(area_id, date, chosen_time_period))

    def f(area_id, date, chosen_time_period):
        url = "https://reservation.bupt.edu.cn/index.php/Wechat/Booking/get_one_day_one_area_state_table_html"

        payload = f"now_area_id={area_id}&query_date={date}&first_room_id=0&start_date={int(datetime.now().strftime('%Y%m%d'))}&the_ajax_execute_times=1"

        headers = {
            'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36",
            'Accept': "application/json, text/javascript, */*; q=0.01",
            'Accept-Encoding': "gzip, deflate, br, zstd",
            'Content-Type': "application/x-www-form-urlencoded",
            'sec-ch-ua': "\"Not/A)Brand\";v=\"8\", \"Chromium\";v=\"126\", \"Google Chrome\";v=\"126\"",
            'x-requested-with': "XMLHttpRequest",
            'sec-ch-ua-mobile': "?0",
            'sec-ch-ua-platform': "\"Windows\"",
            'origin': "https://reservation.bupt.edu.cn",
            'sec-fetch-site': "same-origin",
            'sec-fetch-mode': "cors",
            'sec-fetch-dest': "empty",
            'referer': "https://reservation.bupt.edu.cn/index.php/Wechat/Booking/choose_template/template/1/area_id/5982/country_id/0/from/",
            'accept-language': "zh-CN,zh;q=0.9",
            'priority': "u=1, i",
            'Cookie': f"PHPSESSID={PHPSESSID}"
        }

        response = requests.post(url, data=payload, headers=headers)
        # print(response.text)
        if response.text == "参数错误":
            return None

        js = response.json()
        rooms = js["data"]["rooms"]
        res = {}
        for room in rooms:
            room_id = room["id"]
            # print(room_id)
            text = json.dumps(room, ensure_ascii=False).replace(" ", "")
            # print(text)
            available = re.findall("max_people\":\{(.*?)},", text)[0].split(",")
            tags = room["tag"]
            notBooked = []
            # print(tags)
            for tag in tags.keys():
                # print(tag)
                # print(room_id)
                tag_id = re.findall(f'{room_id}_(\d+)$', tag)
                if tags[tag] == "不可预约":
                    notBooked.append(int(tag_id[0]))
            # print(notBooked)
            max = {}
            for items in available:
                # id = re.findall('max_people_20241102_15415_(.*?)"',items)[0]
                id = int(re.findall(f'{room_id}_(.*?)"', items)[0])
                num = int(items.split(":")[1].replace(" ", "").replace('"', ""))
                if num == 0 or id not in chosen_time_period or id in notBooked:
                    continue
                max[id] = num

            s1 = text.replace(" ", "").replace("\n", "")
            s1 = re.findall('already_reserve\":\{(.*?)}', s1)[0].split(",")
            already_reserve = {}
            for str1 in s1:
                str1 = str1.replace('"', "").split(":")
                # print(int(str1[1]))
                # print(list(max.keys()))
                if int(str1[0]) in list(max.keys()):
                    already_reserve[int(str1[0])] = int(str1[1])

            print(max)
            print(already_reserve)

            for i in list(max.keys()):
                if already_reserve[i] < max[i]:
                    if res.get(i) != None:
                        res[i] = res[i].append(room_id)
                    else:
                        res[i] = [room_id]
            # print(res)

        print(res)

        if res != {}:

            global sign
            sign = 1
            isSuccess = 0
            for i in list(res.keys()):
                pass
                for room_id in res[i]:
                    isSuccess = get_balance_badminton(badminton.index(room_id) + 1, i, date)
            sign = 0

            if isSuccess == 1:
                sendToWechat("抢到羽毛球场了")
            else:
                sendToWechat("羽毛球有空场，可能没抢到")

            schedule.cancel_job(job)

        return res

    # while True:
    #     if sign1 != 1:
    #         schedule.run_pending()
    #     else:
    #         break
    run_schedule()


def update_timetable(area_id, date):
    print(date)
    time_slot = {}
    url = "https://reservation.bupt.edu.cn/index.php/Wechat/Booking/get_one_day_one_area_state_table_html"

    payload = f"now_area_id={area_id}&query_date={date}&first_room_id=0&start_date={int(datetime.now().strftime('%Y%m%d'))}&the_ajax_execute_times=1"

    headers = {
        'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36",
        'Accept': "application/json, text/javascript, */*; q=0.01",
        'Accept-Encoding': "gzip, deflate, br, zstd",
        'Content-Type': "application/x-www-form-urlencoded",
        'sec-ch-ua': "\"Not/A)Brand\";v=\"8\", \"Chromium\";v=\"126\", \"Google Chrome\";v=\"126\"",
        'x-requested-with': "XMLHttpRequest",
        'sec-ch-ua-mobile': "?0",
        'sec-ch-ua-platform': "\"Windows\"",
        'origin': "https://reservation.bupt.edu.cn",
        'sec-fetch-site': "same-origin",
        'sec-fetch-mode': "cors",
        'sec-fetch-dest': "empty",
        'referer': "https://reservation.bupt.edu.cn/index.php/Wechat/Booking/choose_template/template/1/area_id/5982/country_id/0/from/",
        'accept-language': "zh-CN,zh;q=0.9",
        'priority': "u=1, i",
        'Cookie': f"PHPSESSID={PHPSESSID}"
    }

    response = requests.post(url, data=payload, headers=headers)
    if response.text == "参数错误":
        return None


    js = response.json()
    rooms = js["data"]["rooms"]
    for room in rooms:
        room_id = room["id"]
        text = json.dumps(room, ensure_ascii=False).replace(" ", "")
        tags = room["tag"]
        notBooked = []
        for tag in tags.keys():
            tag_id = re.findall(f'{room_id}_(\d+)$', tag)
            if tags[tag] == "不可预约":
                notBooked.append(int(tag_id[0]))

    res = re.findall("time_name\":\{(.*?)},", response.text)[0].split(",")
    available = re.findall("max_people\":\{(.*?)},", response.text)[0]
    matches = re.findall(r'"max_people_[0-9_]+_[0-9_]+_([0-9_]+)":"(?!0\b)[0-9]+"', available)

    for time_id in res:
        item = time_id.split(':"')
        id = int(item[0].replace('"', "").split("15418_")[1])
        time_period = item[1].replace('"', "")
        if id in notBooked:
            continue
        if str(id) in matches:
            time_slot[id] = time_period

    with open('time.json', 'w', encoding='utf-8') as f:
        json.dump(time_slot, f, ensure_ascii=False, indent=4)
    return time_slot


def check_captcha(room_id):
    url = "https://reservation.bupt.edu.cn/index.php/Wechat/Booking/ajax_get_room_reserve_times"

    payload = f"room_id={room_id}"

    headers = {
        'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/116.0.0.0 Safari/537.36 NetType/WIFI MicroMessenger/7.0.20.1781(0x6700143B) "
                      "WindowsWechat(0x63090b17) XWEB/9185 Flue",
        'Accept': "application/json, text/javascript, */*; q=0.01",
        'Content-Type': "application/x-www-form-urlencoded",
        'x-requested-with': "XMLHttpRequest",
        'origin': "https://reservation.bupt.edu.cn",
        'sec-fetch-site': "same-origin",
        'sec-fetch-mode': "cors",
        'sec-fetch-dest': "empty",
        'accept-language': "zh-CN,zh;q=0.9",
        'Cookie': f"PHPSESSID={PHPSESSID}"
    }

    response = requests.post(url, data=payload, headers=headers)

    return response.json()["is_open_reserve_captcha"]


def get_valid_value(area_id, room_id, time_id, date):
    cookies = {
        'PHPSESSID': PHPSESSID,
    }

    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,'
                  'application/signed-exchange;v=b3;q=0.7',
        'accept-language': 'zh-CN,zh;q=0.9',
        'cache-control': 'no-cache',
        'pragma': 'no-cache',
        'priority': 'u=0, i',
        'referer': 'https://reservation.bupt.edu.cn/index.php/Wechat/Show/user',
        'sec-ch-ua': '"Chromium";v="124", "Google Chrome";v="124", "Not-A.Brand";v="99"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'document',
        'sec-fetch-site': 'none',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/116.0.0.0 Safari/537.36 NetType/WIFI MicroMessenger/7.0.20.1781(0x6700143B) '
                      'WindowsWechat(0x6309092b) XWEB/9079 Flue',
    }

    params = {
        'area_id': area_id,
        'td_id': room_id + '_' + time_id,
        'query_date': date,
        'country_id': '0',
    }

    response = requests.get(
        'https://reservation.bupt.edu.cn/index.php/Wechat/Booking/confirm_booking',
        params=params,
        cookies=cookies,
        headers=headers,
    )
    value = re.findall("id='form_valid_code_value' value=\"(.*?)\"", response.text)[0]
    return value


def pay(time_id, room_name, room_id, ticket):
    url = "https://reservation.bupt.edu.cn/index.php/Wechat/Register/register_show"
    cookie = {
        "PHPSESSID": PHPSESSID,
        "think_language": "zh-CN",
    }
    headers = {
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,"
                  "application/signed-exchange;v=b3;q=0.7",
        "accept-language": "zh-CN,zh;q=0.9",
        "cache-control": "no-cache",
        "content-type": "multipart/form-data; boundary=----WebKitFormBoundaryfAtVbB67k98OsEGW",
        "pragma": "no-cache",
        "priority": "u=0, i",
        "sec-ch-ua": "\"Chromium\";v=\"124\", \"Google Chrome\";v=\"124\", \"Not-A.Brand\";v=\"99\"",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "\"Windows\"",
        "sec-fetch-dest": "iframe",
        "sec-fetch-mode": "document",
        "sec-fetch-site": "none",
        "sec-fetch-user": "?1",
        "upgrade-insecure-requests": "1",
        # "cookie": "think_language=; PHPSESSID=" + PHPSESSID,
        "Referrer-Policy": "strict-origin-when-cross-origin"
    }

    # while datetime.now().strftime("%H") != '10':
    #     pass
    # while int(datetime.now().strftime("%S")) < 1:
    #     pass

    if sign == 0:
        while int(datetime.now().strftime("%H")) < 10:
            continue
    valid_value = get_valid_value("5982", room_id, time_id, time_id[0:6])
    print(valid_value)

    data = f'------WebKitFormBoundaryfAtVbB67k98OsEGW\r\nContent-Disposition: form-data; ' \
           f'name=\"form_valid_code_value\"\r\n\r\n{valid_value}\r\n------WebKitFormBoundaryfAtVbB67k98OsEGW\r\nContent' \
           f'-Disposition: form-data; name=\"custom_class_ids\"\r\n\r\n\r\n------WebKitFormBoundaryfAtVbB67k98OsEGW\r' \
           f'\nContent-Disposition: form-data; ' \
           f'name=\"country_id\"\r\n\r\n\r\n------WebKitFormBoundaryfAtVbB67k98OsEGW\r\nContent-Disposition: ' \
           f'form-data; name=\"country_name\"\r\n\r\n\r\n------WebKitFormBoundaryfAtVbB67k98OsEGW\r\nContent' \
           f'-Disposition: form-data; name=\"area_id\"\r\n\r\n5982\r\n------WebKitFormBoundaryfAtVbB67k98OsEGW\r' \
           f'\nContent-Disposition: form-data; ' \
           f'name=\"area_name\"\r\n\r\n一层羽毛球场\r\n------WebKitFormBoundaryfAtVbB67k98OsEGW\r\nContent-Disposition: ' \
           f'form-data; name=\"room_id\"\r\n\r\n{room_id}\r\n------WebKitFormBoundaryfAtVbB67k98OsEGW\r\nContent' \
           f'-Disposition: form-data; name=\"room_name\"\r\n\r\n{room_name}\r\n------WebKitFormBoundaryfAtVbB67k98OsEGW\r' \
           f'\nContent-Disposition: form-data; ' \
           f'name=\"is_open_reserve_captcha\"\r\n\r\n1\r\n------WebKitFormBoundaryfAtVbB67k98OsEGW\r\nContent' \
           f'-Disposition: form-data; name=\"device_id\"\r\n\r\n0\r\n------WebKitFormBoundaryfAtVbB67k98OsEGW\r' \
           f'\nContent-Disposition: form-data; ' \
           f'name=\"selected_device_name\"\r\n\r\n\r\n------WebKitFormBoundaryfAtVbB67k98OsEGW\r\nContent-Disposition' \
           f': form-data; name=\"soft_id\"\r\n\r\n0\r\n------WebKitFormBoundaryfAtVbB67k98OsEGW\r\nContent' \
           f'-Disposition: form-data; name=\"selected_soft_name\"\r\n\r\n\r\n------WebKitFormBoundaryfAtVbB67k98OsEGW' \
           f'\r\nContent-Disposition: form-data; ' \
           f'name=\"time_id\"\r\n\r\n{time_id}\r\n------WebKitFormBoundaryfAtVbB67k98OsEGW\r\nContent-Disposition: ' \
           f'form-data; name=\"total_amount\"\r\n\r\n50\r\n------WebKitFormBoundaryfAtVbB67k98OsEGW\r\nContent' \
           f'-Disposition: form-data; name=\"times_arr\"\r\n\r\nArray\r\n------WebKitFormBoundaryfAtVbB67k98OsEGW\r' \
           f'\nContent-Disposition: form-data; ' \
           f'name=\"packages_showing_type\"\r\n\r\n2\r\n------WebKitFormBoundaryfAtVbB67k98OsEGW\r\nContent' \
           f'-Disposition: form-data; ' \
           f'name=\"mixed_payment_type\"\r\n\r\nwechat_pay\r\n------WebKitFormBoundaryfAtVbB67k98OsEGW\r\nContent' \
           f'-Disposition: form-data; name=\"to_use_vip_id\"\r\n\r\n0\r\n------WebKitFormBoundaryfAtVbB67k98OsEGW\r' \
           f'\nContent-Disposition: form-data; ' \
           f'name=\"request_id\"\r\n\r\na4b966ea19631e7b39aff2e48e66b5c3\r\n------WebKitFormBoundaryfAtVbB67k98OsEGW' \
           f'\r\nContent-Disposition: form-data; ' \
           f'name=\"times_arr_1\"\r\n\r\n08:00-09:00\r\n------WebKitFormBoundaryfAtVbB67k98OsEGW\r\nContent' \
           f'-Disposition: form-data; ' \
           f'name=\"times_arr_2\"\r\n\r\n09:00-10:00\r\n------WebKitFormBoundaryfAtVbB67k98OsEGW\r\nContent' \
           f'-Disposition: form-data; ' \
           f'name=\"times_arr_3\"\r\n\r\n10:00-11:00\r\n------WebKitFormBoundaryfAtVbB67k98OsEGW\r\nContent' \
           f'-Disposition: form-data; ' \
           f'name=\"times_arr_4\"\r\n\r\n11:00-12:00\r\n------WebKitFormBoundaryfAtVbB67k98OsEGW\r\nContent' \
           f'-Disposition: form-data; ' \
           f'name=\"times_arr_5\"\r\n\r\n11:15-12:00\r\n------WebKitFormBoundaryfAtVbB67k98OsEGW\r\nContent' \
           f'-Disposition: form-data; ' \
           f'name=\"times_arr_6\"\r\n\r\n12:00-12:45\r\n------WebKitFormBoundaryfAtVbB67k98OsEGW\r\nContent' \
           f'-Disposition: form-data; ' \
           f'name=\"times_arr_7\"\r\n\r\n12:00-13:00\r\n------WebKitFormBoundaryfAtVbB67k98OsEGW\r\nContent' \
           f'-Disposition: form-data; ' \
           f'name=\"times_arr_8\"\r\n\r\n13:00-14:00\r\n------WebKitFormBoundaryfAtVbB67k98OsEGW\r\nContent' \
           f'-Disposition: form-data; ' \
           f'name=\"times_arr_9\"\r\n\r\n14:00-15:00\r\n------WebKitFormBoundaryfAtVbB67k98OsEGW\r\nContent' \
           f'-Disposition: form-data; ' \
           f'name=\"times_arr_10\"\r\n\r\n15:00-16:00\r\n------WebKitFormBoundaryfAtVbB67k98OsEGW\r\nContent' \
           f'-Disposition: form-data; ' \
           f'name=\"times_arr_11\"\r\n\r\n16:00-17:00\r\n------WebKitFormBoundaryfAtVbB67k98OsEGW\r\nContent' \
           f'-Disposition: form-data; ' \
           f'name=\"times_arr_12\"\r\n\r\n17:00-18:00\r\n------WebKitFormBoundaryfAtVbB67k98OsEGW\r\nContent' \
           f'-Disposition: form-data; ' \
           f'name=\"times_arr_13\"\r\n\r\n18:00-19:00\r\n------WebKitFormBoundaryfAtVbB67k98OsEGW\r\nContent' \
           f'-Disposition: form-data; ' \
           f'name=\"times_arr_14\"\r\n\r\n19:00-20:00\r\n------WebKitFormBoundaryfAtVbB67k98OsEGW\r\nContent' \
           f'-Disposition: form-data; ' \
           f'name=\"times_arr_15\"\r\n\r\n20:00-21:00\r\n------WebKitFormBoundaryfAtVbB67k98OsEGW\r\nContent' \
           f'-Disposition: form-data; ' \
           f'name=\"times_arr_16\"\r\n\r\n21:00-22:00\r\n------WebKitFormBoundaryfAtVbB67k98OsEGW\r\nContent' \
           f'-Disposition: form-data; name=\"is_queue\"\r\n\r\n0\r\n------WebKitFormBoundaryfAtVbB67k98OsEGW\r' \
           f'\nContent-Disposition: form-data; ' \
           f'name=\"randstr\"\r\n\r\n@F2D\r\n------WebKitFormBoundaryfAtVbB67k98OsEGW\r\nContent-Disposition: ' \
           f'form-data; ' \
           f'name=\"ticket\"\r\n\r' \
           f'\n{ticket}\r\n------WebKitFormBoundaryfAtVbB67k98OsEGW\r\nContent-Disposition: form-data; ' \
           f'name=\"occupy_quota\"\r\n\r\n1\r\n------WebKitFormBoundaryfAtVbB67k98OsEGW\r\nContent-Disposition: ' \
           f'form-data; name=\"sign_and_login_type\"\r\n\r\n1\r\n------WebKitFormBoundaryfAtVbB67k98OsEGW--\r\n '


    response = requests.post(url, headers=headers, data=data.encode("utf-8"), cookies=cookie)

    if "北邮体育馆" in response.text:
        print("success")
        return False
    else:
        print(response.text)
        return True


def get_balance_badminton(id, times, date):
    # id是羽毛球场编号，如要预定“羽毛球场1号”，则id=1
    # time是时间段，在time.txt中查表得到，如要预定“08:00-09:00"时间段的场，则time=1
    # date是要预定的日期，date=“20180205”表明要预约2018年2月5号的场次

    url = "https://reservation.bupt.edu.cn/index.php/Wechat/Booking/get_one_day_one_area_state_table_html"

    payload = f"now_area_id=5982&query_date={date}&first_room_id=0&start_date={datetime.now().strftime('%Y%m%d')}&the_ajax_execute_times=2"

    headers = {
        'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36",
        'Accept': "application/json, text/javascript, */*; q=0.01",
        'Accept-Encoding': "gzip, deflate, br, zstd",
        'Content-Type': "application/x-www-form-urlencoded",
        'sec-ch-ua': "\"Not/A)Brand\";v=\"8\", \"Chromium\";v=\"126\", \"Google Chrome\";v=\"126\"",
        'x-requested-with': "XMLHttpRequest",
        'sec-ch-ua-mobile': "?0",
        'sec-ch-ua-platform': "\"Windows\"",
        'origin': "https://reservation.bupt.edu.cn",
        'sec-fetch-site': "same-origin",
        'sec-fetch-mode': "cors",
        'sec-fetch-dest': "empty",
        'accept-language': "zh-CN,zh;q=0.9",
        'priority': "u=1, i",
        'Cookie': f"PHPSESSID={PHPSESSID}"
    }

    response = requests.post(url, data=payload, headers=headers)

    cookies = {
        'PHPSESSID': PHPSESSID,
        'think_language': 'zh-cn',
    }
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36 NetType/WIFI MicroMessenger/7.0.20.1781(0x6700143B) WindowsWechat(0x6309092b) XWEB/9079 Flue',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'Content-Type': 'application/x-www-form-urlencoded',
        'pragma': 'no-cache',
        'cache-control': 'no-cache',
        'sec-ch-ua': '"Chromium";v="122", "Not(A:Brand";v="24", "Google Chrome";v="122"',
        'x-requested-with': 'XMLHttpRequest',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'origin': 'https://reservation.bupt.edu.cn',
        'sec-fetch-site': 'none',
        'sec-fetch-mode': 'document',
        'sec-fetch-dest': 'empty',
        'accept-language': 'zh-CN,zh;q=0.9',
        'upgrade-insecure-requests': '1',
    }
    if times < 10:
        times = "0" + str(times)
    else:
        times = str(times)

    # time_id = ""
    # for time in times:
    #     if int(time) < 10:
    #         time = "0" + time
    #     time_id += str(date) + time + " "

    data = {
        'room_id': badminton[id - 1],  # 选场
        'device_id': '0',
        'soft_id': '0',
        'time_id': str(date) + times,  # 选时间
        # 'time_id': time_id,  # 选时间
        'area_id': '5982',  # 羽毛球场id
        'card_id': '0',
        'card_name': '0',
        'card_type': '0',
        'card_discount': '0',
        'finall_price': '50',
        'occupy_quota': '1',
    }

    response = requests.post(
        'https://reservation.bupt.edu.cn/index.php/Wechat/MixedPayment/get_balance_and_packages_of_one_user',
        cookies=cookies,
        headers=headers,
        data=data,
    )
    name = "羽毛球场" + str(id) + "号"

    is_captcha = check_captcha(badminton[id - 1])
    print(is_captcha)

    if is_captcha == 0:
        pay(str(date) + times, name, badminton[id - 1], "")
    else:
        lock.acquire()
        try:
            ticket = TecentSliderVerify.slider()
        finally:
            lock.release()
        pay(str(date) + times, name, badminton[id - 1], ticket)


def modify_phpsessid(new_phpsessid):
    global PHPSESSID
    PHPSESSID = new_phpsessid
    with open("./PHPSESSID.txt", "w") as f1:
        f1.write(new_phpsessid)
    messagebox.showinfo("成功", "PHPSESSID已更新")


def run_update_timetable():
    area_id = 5982
    #date = int((datetime.now() + timedelta(days=1)).strftime('%Y%m%d'))
    date = date_entry.get()

    global time_slots
    time_slots = update_timetable(area_id, date)
    print(time_slots)
    # if time_slots:
    #     messagebox.showinfo("成功", f"成功")


def run_get_balance_gym(selected_areas, selected_times, date):
    with ThreadPoolExecutor(max_workers=4) as executor:
        for area in selected_areas:
            for time in selected_times:
                time = int(time)
                area = int(area)
                date = int(date)
                executor.submit(get_balance_badminton, area, time, date)


root = tk.Tk()
testMode = tk.IntVar(value=0)
root.title("羽毛球")

tk.Label(root, text="选择日期 (YYYYMMDD):").grid(row=0, column=0, sticky='w')
date_entry = tk.Entry(root)
date_entry.insert(0, str(int((datetime.now() + timedelta(days=1)).strftime("%Y%m%d"))))
date_entry.grid(row=0, column=1, columnspan=2, sticky='w')

tk.Label(root, text="选择场次:").grid(row=1, column=0, sticky='w')
area_vars = [tk.IntVar() for _ in range(len(badminton))]
for i, area in enumerate(badminton):
    tk.Checkbutton(root, text=f"{i + 1}号场", variable=area_vars[i]).grid(row=1 + i // 4, column=i % 4 + 1,
                                                                          sticky='w')
    if (i + 1) % 4 == 0:
        row = 1 + (i + 1) // 4

tk.Label(root, text="选择时间段:").grid(row=3, column=0, sticky='w')
time_vars = {key: tk.IntVar() for key in time_slots}
for i, (key, value) in enumerate(time_slots.items()):
    tk.Checkbutton(root, text=value, variable=time_vars[key]).grid(row=4 + i // 4, column=i % 4 + 1, sticky='w')


def on_modify_phpsessid():
    new_session_id = simpledialog.askstring("输入", "请输入新的PHPSESSID:", parent=root)
    if new_session_id is not None:
        try:
            with open("./PHPSESSID.txt", "w") as f:
                f.write(new_session_id)
            messagebox.showinfo("成功", "PHPSESSID已更新。")
            global PHPSESSID
            PHPSESSID = new_session_id
        except Exception as e:
            messagebox.showerror("错误", f"无法写入文件: {e}")


def on_confirm():
    global sign
    sign = testMode.get()
    date = date_entry.get()
    selected_areas = [i + 1 for i, var in enumerate(area_vars) if var.get()]
    selected_times = [key for key, var in time_vars.items() if var.get()]

    if not date:
        messagebox.showwarning("输入错误", "请输入日期")
        return

    if not selected_areas:
        messagebox.showwarning("输入错误", "请选择至少一个场次")
        return

    if not selected_times:
        messagebox.showwarning("输入错误", "请选择至少一个时间段")
        return

    if len(selected_times) * len(selected_areas) > 4:
        messagebox.showwarning("场次太多", "选择场次太多容易出错哦\n建议不超过四个")
        return

    # if len(selected_areas) > 1 and len(selected_times) > 1:
    #     messagebox.showwarning("输入错误", "场次和时间段至多一个可以多选")
    #     return
    if testMode.get() == 0:
        while int(datetime.now().strftime("%M")) <= 58:
            continue
    run_get_balance_gym(selected_areas, selected_times, date)


modify_button = tk.Button(root, text="修改PHPSESSID", command=on_modify_phpsessid)
modify_button.grid(row=8, column=0, pady=10, sticky='w')

update_timetable_button = tk.Button(root, text="更新时间表", command=run_update_timetable)
update_timetable_button.grid(row=8, column=1, pady=10, sticky='w')

time_mode_checkbox = tk.Checkbutton(root, text="测试模式", variable=testMode, onvalue=1, offvalue=0)
time_mode_checkbox.grid(row=8, column=3, pady=10, sticky='w')

confirm_button = tk.Button(root, text="开抢", command=on_confirm)
confirm_button.grid(row=8, column=2, pady=10, sticky='w')


def open_time_selection():
    run_update_timetable()
    # 创建新窗口
    time_window = tk.Toplevel(root)
    time_window.title("选择时间段")

    # 获取屏幕的宽度和高度
    screen_width = time_window.winfo_screenwidth()
    screen_height = time_window.winfo_screenheight()

    # 设置新窗口的宽度和高度
    window_width = 400
    window_height = 300

    # 计算居中位置
    x = (screen_width // 2) - (window_width // 2)
    y = (screen_height // 2) - (window_height // 2)

    # 设置新窗口的位置和大小
    time_window.geometry(f"{window_width}x{window_height}+{x}+{y}")

    # 存储选中的时间段
    selected_times = []

    def on_confirm1():
        selected = [time_id for time_id, var in time_vars.items() if var.get()]
        print(selected)
        selected_times.clear()
        selected_times.extend(selected)

        time_window.destroy()
        check_empty(5982, int(date_entry.get()), selected)

    def toggle_select_all():
        # 设置所有复选框的值为全选框的值
        select_all_value = select_all_var.get()
        for var in time_vars.values():
            var.set(select_all_value)

    select_all_var = tk.IntVar()
    select_all_cb = tk.Checkbutton(time_window, text="全选", variable=select_all_var, command=toggle_select_all)
    select_all_cb.grid(row=0, column=0, columnspan=4, sticky='w')  # 全选框占据第一行

    # 创建多选框
    time_vars = {}
    for idx, (time_id, time) in enumerate(time_slots.items()):
        var = tk.IntVar()
        cb = tk.Checkbutton(time_window, text=time, variable=var)
        cb.grid(row=(idx // 4) + 1, column=idx % 4, sticky='ew')  # 使多选框占满整一行
        time_vars[time_id] = var  # 使用时间段 ID 作为键

    # 设置每列的权重，以便均匀分布
    for col in range(4):
        time_window.grid_columnconfigure(col, weight=1)

    # 确定按钮
    confirm_button = tk.Button(time_window, text="确定", command=on_confirm1)
    confirm_button.grid(row=(len(time_slots) // 4) + 2, column=0, columnspan=4, pady=10)  # 按钮不占满整行


def change_period():

    # 弹出输入框窗口
    entry_window = tk.Toplevel(root)
    entry_window.title("更改间隔")

    window_width, window_height = 300, 150
    screen_width = entry_window.winfo_screenwidth()
    screen_height = entry_window.winfo_screenheight()
    position_x = (screen_width - window_width) // 2
    position_y = (screen_height - window_height) // 2
    entry_window.geometry(f"{window_width}x{window_height}+{position_x}+{position_y}")

    tk.Label(entry_window, text="请输入间隔(s):").pack(pady=(10, 0))
    entry = tk.Entry(entry_window)
    entry.pack(pady=(5, 10))

    def update_variable():
        global check_period
        check_period = int(entry.get())
        entry_window.destroy()  # 关闭输入框窗口

    confirm_button = tk.Button(entry_window, text="确认", command=update_variable)
    confirm_button.pack(pady=(5, 10))


check_button = tk.Button(root, text="捡漏模式", command=open_time_selection)
check_button.grid(row=9, column=2, pady=10, sticky='w')

edit_button = tk.Button(root, text="修改间隔 ", command=change_period)
edit_button.grid(row=9, column=3, pady=10, sticky='w')

width = 550
height = 300
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
# Find the center position
center_x = int(screen_width / 2 - width / 2)
center_y = int(screen_height / 2 - height / 2)
# Set the position of the window to the center of the screen
root.geometry(f'{width}x{height}+{center_x}+{center_y}')

root.mainloop()
