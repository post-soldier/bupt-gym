import re
import tkinter as tk
from tkinter import simpledialog, messagebox, ttk
from datetime import datetime, timedelta
import requests
import json
import schedule

import TecentSliderVerify

with open("./PHPSESSID.txt", "r") as f1:
    PHPSESSID = f1.read()

with open('time.json', 'r', encoding='utf-8') as f:
    time_slots = json.load(f)

time_slots = {int(k): v for k, v in time_slots.items()}



sign = 0

check_period = 15

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


def check_empty(area_id, date, chosen_time_period):
    print(check_period)
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

            max = {}
            for items in available:
                # id = re.findall('max_people_20241102_15415_(.*?)"',items)[0]
                # print(id)
                id = int(re.findall(f'{room_id}_(.*?)"', items)[0])
                num = int(items.split(":")[1].replace(" ", "").replace('"', ""))
                if num == 0 or id not in chosen_time_period:
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
                isSuccess = get_balance_gym(i, date)
            sign = 0

            if isSuccess == 1:
                sendToWechat("抢到健身房的场了")
            else:
                sendToWechat("健身房有空场，可能没抢到")

            schedule.cancel_job(job)

        return res

    # while True:
    #     if sign1 != 1:
    #         schedule.run_pending()
    #     else:
    #         break
    run_schedule()


def update_timetable(area_id, date):
    with open("./PHPSESSID.txt", "r") as f1:
        global PHPSESSID
        PHPSESSID = f1.read()

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
    # print(response.text)
    if response.text == "参数错误":
        return None

    res = re.findall("time_name\":\{(.*?)},", response.text)[0].split(",")
    available = re.findall("max_people\":\{(.*?)},", response.text)[0]
    matches = re.findall(r'"max_people_[0-9_]+_[0-9_]+_([0-9_]+)":"(?!0\b)[0-9]+"', available)

    for time_id in res:
        item = time_id.split(':"')
        id = int(item[0].replace('"', "").split("15415_")[1])
        time_period = item[1].replace('"', "")
        if str(id) in matches:
            time_slot[id] = time_period

    with open('time.json', 'w', encoding='utf-8') as f:
        json.dump(time_slot, f, ensure_ascii=False, indent=4)

    return time_slot


def check_captcha(room_id):
    url = "https://reservation.bupt.edu.cn/index.php/Wechat/Booking/ajax_get_room_reserve_times"

    payload = f"room_id={room_id}"

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
        'referer': "https://reservation.bupt.edu.cn/index.php/Wechat/Booking/choose_template/template/1/area_id/5985/country_id/0",
        'accept-language': "zh-CN,zh;q=0.9",
        'priority': "u=0, i",
        'Cookie': f"PHPSESSID={PHPSESSID}"
    }

    response = requests.post(url, data=payload, headers=headers)
    # response = client.post(url, data=payload, headers=headers)

    return response.json()["is_open_reserve_captcha"]


def get_valid_value(area_id, room_id, time_id, year_month):
    cookies = {
        'PHPSESSID': PHPSESSID,
    }

    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
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
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36 NetType/WIFI MicroMessenger/7.0.20.1781(0x6700143B) WindowsWechat(0x6309092b) XWEB/9079 Flue',
    }

    params = {
        'area_id': area_id,
        'td_id': room_id + '_' + time_id,
        'query_date': year_month,
        'country_id': '0',
    }

    response = requests.get(
        'https://reservation.bupt.edu.cn/index.php/Wechat/Booking/confirm_booking',
        params=params,
        cookies=cookies,
        headers=headers,
    )
    # response = client.get(
    #     'https://reservation.bupt.edu.cn/index.php/Wechat/Booking/confirm_booking',
    #     params=params,
    #     cookies=cookies,
    #     headers=headers,
    # )

    value = re.findall("id='form_valid_code_value' value=\"(.*?)\"", response.text)[0]
    price = re.findall('id=\"no_card_price\" value=\"(.*?)\"', response.text)[0]
    return value, price



def pay(time_id, ticket):
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
        "content-type": "multipart/form-data; boundary=----WebKitFormBoundary1FOdTJeAgQAaYSJ0",
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

    # while datetime.now().strftime("%H") != '12':
    #     pass
    # #
    # while int(datetime.now().strftime("%S")) < 1:
    #     pass

    if sign == 0:
        while int(datetime.now().strftime("%H")) < 12:
            continue

        while int(datetime.now().strftime("%S")) < 1:
            continue
    valid_value,price = get_valid_value("5985", "15415", time_id, time_id[0:6])

    print(time_id)
    print(valid_value)
    data = f'------WebKitFormBoundary1FOdTJeAgQAaYSJ0\r\nContent-Disposition: form-data; ' \
           f'name=\"form_valid_code_value\"\r\n\r\n{valid_value}\r\n------WebKitFormBoundary1FOdTJeAgQAaYSJ0\r\nContent' \
           f'-Disposition: form-data; name=\"custom_class_ids\"\r\n\r\n\r\n------WebKitFormBoundary1FOdTJeAgQAaYSJ0\r' \
           f'\nContent-Disposition: form-data; name=\"country_id\"\r\n\r\n\r\n------WebKitFormBoundary1FOdTJeAgQAaYSJ0\r' \
           f'\nContent-Disposition: form-data; name=\"country_name\"\r\n\r\n\r\n------WebKitFormBoundary1FOdTJeAgQAaYSJ0' \
           f'\r\nContent-Disposition: form-data; name=\"area_id\"\r\n\r\n5985\r\n------WebKitFormBoundary1FOdTJeAgQAaYSJ0' \
           f'\r\nContent-Disposition: form-data; ' \
           f'name=\"area_name\"\r\n\r\n健身房\r\n------WebKitFormBoundary1FOdTJeAgQAaYSJ0\r\nContent-Disposition: form-data; ' \
           f'name=\"room_id\"\r\n\r\n15415\r\n------WebKitFormBoundary1FOdTJeAgQAaYSJ0\r\nContent-Disposition: form-data; ' \
           f'name=\"room_name\"\r\n\r\n健身房\r\n------WebKitFormBoundary1FOdTJeAgQAaYSJ0\r\nContent-Disposition: form-data; ' \
           f'name=\"is_open_reserve_captcha\"\r\n\r\n1\r\n------WebKitFormBoundary1FOdTJeAgQAaYSJ0\r\nContent-Disposition' \
           f': form-data; name=\"device_id\"\r\n\r\n0\r\n------WebKitFormBoundary1FOdTJeAgQAaYSJ0\r\nContent-Disposition: ' \
           f'form-data; name=\"selected_device_name\"\r\n\r\n\r\n------WebKitFormBoundary1FOdTJeAgQAaYSJ0\r\nContent' \
           f'-Disposition: form-data; name=\"soft_id\"\r\n\r\n0\r\n------WebKitFormBoundary1FOdTJeAgQAaYSJ0\r\nContent' \
           f'-Disposition: form-data; name=\"selected_soft_name\"\r\n\r\n\r\n------WebKitFormBoundary1FOdTJeAgQAaYSJ0\r' \
           f'\nContent-Disposition: form-data; ' \
           f'name=\"time_id\"\r\n\r\n{time_id}\r\n------WebKitFormBoundary1FOdTJeAgQAaYSJ0\r\nContent-Disposition: ' \
           f'form-data; name=\"total_amount\"\r\n\r\n{price}\r\n------WebKitFormBoundary1FOdTJeAgQAaYSJ0\r\nContent' \
           f'-Disposition: form-data; name=\"times_arr\"\r\n\r\nArray\r\n------WebKitFormBoundary1FOdTJeAgQAaYSJ0\r' \
           f'\nContent-Disposition: form-data; ' \
           f'name=\"packages_showing_type\"\r\n\r\n2\r\n------WebKitFormBoundary1FOdTJeAgQAaYSJ0\r\nContent-Disposition: ' \
           f'form-data; name=\"mixed_payment_type\"\r\n\r\nwechat_pay\r\n------WebKitFormBoundary1FOdTJeAgQAaYSJ0\r' \
           f'\nContent-Disposition: form-data; ' \
           f'name=\"to_use_vip_id\"\r\n\r\n0\r\n------WebKitFormBoundary1FOdTJeAgQAaYSJ0\r\nContent-Disposition: ' \
           f'form-data; name=\"request_id\"\r\n\r\na4b966ea19631e7b39aff2e48e66b5c3\r\n' \
           f'------WebKitFormBoundary1FOdTJeAgQAaYSJ0\r\nContent-Disposition: form-data; ' \
           f'name=\"times_arr_1\"\r\n\r\n08:00-09:30\r\n------WebKitFormBoundary1FOdTJeAgQAaYSJ0\r\nContent-Disposition: ' \
           f'form-data; name=\"times_arr_2\"\r\n\r\n08:00-09:00\r\n------WebKitFormBoundary1FOdTJeAgQAaYSJ0\r\nContent' \
           f'-Disposition: form-data; name=\"times_arr_3\"\r\n\r\n09:00-10:00\r\n------WebKitFormBoundary1FOdTJeAgQAaYSJ0' \
           f'\r\nContent-Disposition: form-data; ' \
           f'name=\"times_arr_4\"\r\n\r\n10:00-11:00\r\n------WebKitFormBoundary1FOdTJeAgQAaYSJ0\r\nContent-Disposition: ' \
           f'form-data; name=\"times_arr_5\"\r\n\r\n11:00-12:00\r\n------WebKitFormBoundary1FOdTJeAgQAaYSJ0\r\nContent' \
           f'-Disposition: form-data; name=\"times_arr_6\"\r\n\r\n11:00-12:30\r\n------WebKitFormBoundary1FOdTJeAgQAaYSJ0' \
           f'\r\nContent-Disposition: form-data; ' \
           f'name=\"times_arr_7\"\r\n\r\n11:10-12:30\r\n------WebKitFormBoundary1FOdTJeAgQAaYSJ0\r\nContent-Disposition: ' \
           f'form-data; name=\"times_arr_8\"\r\n\r\n12:00-13:00\r\n------WebKitFormBoundary1FOdTJeAgQAaYSJ0\r\nContent' \
           f'-Disposition: form-data; name=\"times_arr_9\"\r\n\r\n13:00-14:00\r\n------WebKitFormBoundary1FOdTJeAgQAaYSJ0' \
           f'\r\nContent-Disposition: form-data; ' \
           f'name=\"times_arr_10\"\r\n\r\n14:00-15:00\r\n------WebKitFormBoundary1FOdTJeAgQAaYSJ0\r\nContent-Disposition: ' \
           f'form-data; name=\"times_arr_11\"\r\n\r\n14:20-15:00\r\n------WebKitFormBoundary1FOdTJeAgQAaYSJ0\r\nContent' \
           f'-Disposition: form-data; ' \
           f'name=\"times_arr_12\"\r\n\r\n15:00-16:00\r\n------WebKitFormBoundary1FOdTJeAgQAaYSJ0\r\nContent-Disposition: ' \
           f'form-data; name=\"times_arr_13\"\r\n\r\n16:00-17:00\r\n------WebKitFormBoundary1FOdTJeAgQAaYSJ0\r\nContent' \
           f'-Disposition: form-data; ' \
           f'name=\"times_arr_14\"\r\n\r\n16:10-17:00\r\n------WebKitFormBoundary1FOdTJeAgQAaYSJ0\r\nContent-Disposition: ' \
           f'form-data; name=\"times_arr_15\"\r\n\r\n17:00-18:00\r\n------WebKitFormBoundary1FOdTJeAgQAaYSJ0\r\nContent' \
           f'-Disposition: form-data; ' \
           f'name=\"times_arr_16\"\r\n\r\n18:00-19:00\r\n------WebKitFormBoundary1FOdTJeAgQAaYSJ0\r\nContent-Disposition: ' \
           f'form-data; name=\"times_arr_17\"\r\n\r\n19:00-20:00\r\n------WebKitFormBoundary1FOdTJeAgQAaYSJ0\r\nContent' \
           f'-Disposition: form-data; ' \
           f'name=\"times_arr_18\"\r\n\r\n20:00-21:00\r\n------WebKitFormBoundary1FOdTJeAgQAaYSJ0\r\nContent-Disposition: ' \
           f'form-data; name=\"times_arr_19\"\r\n\r\n21:00-22:00\r\n------WebKitFormBoundary1FOdTJeAgQAaYSJ0\r\nContent' \
           f'-Disposition: form-data; name=\"is_queue\"\r\n\r\n0\r\n------WebKitFormBoundary1FOdTJeAgQAaYSJ0\r\nContent' \
           f'-Disposition: form-data; name=\"randstr\"\r\n\r\n@kho\r\n------WebKitFormBoundary1FOdTJeAgQAaYSJ0\r\nContent' \
           f'-Disposition: form-data; name=\"ticket\"\r\n\r\n{ticket}\r\n------WebKitFormBoundary1FOdTJeAgQAaYSJ0\r' \
           f'\nContent-Disposition: form-data; name=\"occupy_quota\"\r\n\r\n1\r\n------WebKitFormBoundary1FOdTJeAgQAaYSJ0' \
           f'\r\nContent-Disposition: form-data; ' \
           f'name=\"sign_and_login_type\"\r\n\r\n1\r\n------WebKitFormBoundary1FOdTJeAgQAaYSJ0--\r\n '

    # while int(datetime.now().strftime("%M")) != 46:
    #     continue


    # response = client.post(url, headers=headers, data=data.encode("utf-8"), cookies=cookie)
    response = requests.post(url, headers=headers, data=data.encode("utf-8"), cookies=cookie)
    # print(response.content.decode("utf-8"))

    if "北邮体育馆" in response.text:
        print("success")
        return 1
    elif "400 Bad Request" in response.text or response.text == "":
        print("可能抢到了，去订单页看看")
        return 2
    else:
        # print(response.text)
        print(response.content.decode("utf-8"))
        return 0


def get_balance_gym(time, date):
    # id是羽毛球场编号，如要预定“羽毛球场1号”，则id=1
    # time是时间段，在time.txt中查表得到，如要预定“08:00-09:00"时间段的场，则time=1
    # date是要预定的日期，date=“20180205”表明要预约2018年2月5号的场次

    url = "https://reservation.bupt.edu.cn/index.php/Wechat/Booking/get_one_day_one_area_state_table_html"

    cookie = {
        "PHPSESSID": PHPSESSID,
    }

    # payload = f"now_area_id=5985&query_date={date}&first_room_id=0&start_date={datetime.now().strftime('%Y%m%d')}&the_ajax_execute_times=2"

    data = {
        'now_area_id': "5985",
        "query_date": str(date),
        "first_room_id": "0",
        "start_date": datetime.now().strftime('%Y%m%d'),
        "the_ajax_execute_times": "2",
    }
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
        # 'Cookie': f"PHPSESSID={PHPSESSID}"
    }

    response = requests.post(url, data=data, headers=headers, cookies=cookie)

    is_captcha = check_captcha(15415)

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
    if time < 10:
        time = "0" + str(time)
    else:
        time = str(time)

    data = {
        'room_id': 15415,  # 选场
        'device_id': '0',
        'soft_id': '0',
        'time_id': str(date) + time,  # 选时间
        'area_id': '5985',
        'card_id': '0',
        'card_name': '0',
        'card_type': '0',
        'card_discount': '0',
        'finall_price': '16',
        'occupy_quota': '1',
    }

    response = requests.post(
        'https://reservation.bupt.edu.cn/index.php/Wechat/MixedPayment/get_balance_and_packages_of_one_user',
        cookies=cookies,
        headers=headers,
        data=data,
    )
    # response = client.post(
    #     'https://reservation.bupt.edu.cn/index.php/Wechat/MixedPayment/get_balance_and_packages_of_one_user',
    #     cookies=cookies,
    #     headers=headers,
    #     data=data,
    # )
    # valid_value = get_valid_value("5985", "15415", str(date) + time, str(date))

    if is_captcha == '0':
        return pay(str(date) + time, "")
    else:
        ticket = TecentSliderVerify.slider()
        return pay(str(date) + time, ticket)


def update_session_id():
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


def run_update_timetable():
    area_id = 5985
    # date = int((datetime.now()+timedelta(days=1)).strftime('%Y%m%d'))
    date = int(date_entry.get())
    print(date)

    global time_slots
    time_slots = update_timetable(area_id, date)

    global time_combobox
    time_combobox['values'] = [f"{k}: {v}" for k, v in time_slots.items()]
    time_combobox.set('')  # 清空当前选择，重新选择
    print(time_slots)


def run_get_balance_gym():
    global sign
    sign = testMode.get()
    global PHPSESSID
    with open("./PHPSESSID.txt", "r") as f1:
        PHPSESSID = f1.read()

    session_time = int(time_combobox.get().split(': ')[0])
    date = int(date_entry.get())  # Get the input date
    if session_time and date:
        messagebox.showinfo("提示", "显示未响应是正常的，请不要进行任何操作（包括移动鼠标）\n        点击确定开始")


        if sign == 0:
            while True:
                if int(datetime.now().strftime("%H")) < 11:
                    continue
                if int(datetime.now().strftime("%M")) < 59:
                    continue
                if int(datetime.now().strftime("%S")) < 20:
                    continue
                else:
                    break
            # while int(datetime.now().strftime("%M")) <= 59:
            #     continue
            # while int(datetime.now().strftime("%S")) < 30:
            #     continue
        re = get_balance_gym(session_time, date)
        print(1)
        if re == 1:
            messagebox.showinfo("成功", "成功抢到，请及时进入详情页支付！")
        elif re == 2:
            messagebox.showinfo("??", "可能抢到，请进入详情页查看！")
        else:
            messagebox.showinfo("失败", "对不起，没抢到。")
    else:
        messagebox.showwarning("警告", "请确保日期和场次都已填写。")


def center_window(width=300, height=300):
    # Get the screen dimension
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    # Find the center position
    center_x = int(screen_width / 2 - width / 2)
    center_y = int(screen_height / 2 - height / 2)

    # Set the position of the window to the center of the screen
    root.geometry(f'{width}x{height}+{center_x}+{center_y}')


# Create main window
root = tk.Tk()
root.title("健身房")
center_window(300, 370)
testMode = tk.IntVar(value=0)

# Button to update PHPSESSID
update_button = tk.Button(root, text="更新 PHPSESSID", command=update_session_id)
update_button.pack(pady=(10, 5))

update_timetable_button = tk.Button(root, text="更新时间表", command=run_update_timetable)
update_timetable_button.pack(pady=(5, 10))

# Add a label for instructions
instruction_label1 = tk.Label(root, text="请输入日期（格式：YYYYMMDD）：")
instruction_label1.pack(pady=(10, 5))

# Entry for date
date_entry = tk.Entry(root)
date_entry.insert(0, str(int((datetime.now() + timedelta(days=1)).strftime("%Y%m%d"))))
date_entry.pack(pady=5)

instruction_label2 = tk.Label(root, text="选择时间段：")
instruction_label2.pack(pady=(10, 5))

# Combobox for time slots

time_combobox = ttk.Combobox(root, values=[f"{k}: {v}" for k, v in time_slots.items()])
time_combobox.pack(pady=5)

time_mode_checkbox = tk.Checkbutton(root, text="测试模式", variable=testMode, onvalue=1, offvalue=0)
time_mode_checkbox.pack(pady=(10, 5))

# Button to run get_balance_gym
run_button = tk.Button(root, text="开抢", command=run_get_balance_gym)
run_button.pack(pady=(5, 10))


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
        check_empty(5985, int(date_entry.get()), selected)

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

    default_label = tk.Label(time_window, text="默认间隔15s")
    default_label.grid(row=(len(time_slots) // 4) + 3, column=0, columnspan=4, pady=10)




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


button_frame = tk.Frame(root)
button_frame.pack(pady=(10, 10))

# 创建捡漏模式按钮
check_button = tk.Button(button_frame, text="捡漏模式", command=open_time_selection)
check_button.pack(side="left", padx=(5, 10))

# 创建修改变量按钮
edit_button = tk.Button(button_frame, text="修改间隔 ", command=change_period)
edit_button.pack(side="left", padx=(5, 10))

# Start the GUI
root.mainloop()
