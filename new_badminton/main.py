import tkinter as tk
from tkinter import messagebox, simpledialog
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor
import requests
import re
import slider_verify.TecentSliderVerify
import threading

lock = threading.Lock()
# 读取PHPSESSID
with open("../PHPSESSID.txt", "r") as f1:
    PHPSESSID = f1.read()

badminton = ["15418", "15419", "15420", "15421", "15422", "15423", "15424", "15425", "15426"]

time_slots = {
    1: "08:00-09:00",
    2: "09:00-10:00",
    3: "10:00-11:00",
    4: "11:00-12:00",
    6: "12:00-13:00",
    7: "13:00-14:00",
    8: "14:00-15:00",
    9: "15:00-16:00",
    10: "16:00-17:00",
    11: "17:00-18:00",
    12: "18:00-19:00",
    13: "19:00-20:00",
    14: "20:00-21:00",
    15: "21:00-22:00"
}


def get_valid_value(area_id, room_id, time_id, date):
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
    is_open_reserve_captcha = re.findall("id='is_open_reserve_captcha' value=\"(.*?)\"", response.text)[0]
    return value, is_open_reserve_captcha


def pay(time_id, room_name, room_id, ticket, valid_value):
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
           f'form-data; name=\"total_amount\"\r\n\r\n20\r\n------WebKitFormBoundaryfAtVbB67k98OsEGW\r\nContent' \
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

    while datetime.now().strftime("%H") != '10':
        pass
    response = requests.post(url, headers=headers, data=data, cookies=cookie)

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
        'finall_price': '0',
        'occupy_quota': '1',
    }

    response = requests.post(
        'https://reservation.bupt.edu.cn/index.php/Wechat/MixedPayment/get_balance_and_packages_of_one_user',
        cookies=cookies,
        headers=headers,
        data=data,
    )
    name = "羽毛球场" + str(id) + "号"
    # with open("main.js", "r", encoding="utf-8") as f:
    #     js = f.read()

    valid_value, is_captcha = get_valid_value("5982", badminton[id - 1], str(date) + times, str(date))

    print(valid_value)
    print(is_captcha)

    if is_captcha == 0:
        pay(str(date) + times, name, badminton[id - 1], "", valid_value)
    else:
        lock.acquire()
        try:
            ticket = slider_verify.TecentSliderVerify.slider()
        finally:
            lock.release()
        pay(str(date) + times, name, badminton[id - 1], ticket, valid_value)

    # ctx = execjs.compile(js).call("main", PHPSESSID, "一层羽毛球场", 5982, name, badminton[id - 1], str(date) + time,ticket, 50)
    # 50ms请求一次


def modify_phpsessid(new_phpsessid):
    global PHPSESSID
    PHPSESSID = new_phpsessid
    with open("../PHPSESSID.txt", "w") as f1:
        f1.write(new_phpsessid)
    messagebox.showinfo("成功", "PHPSESSID已更新")


def run_get_balance_gym(selected_areas, selected_times, date):
    with ThreadPoolExecutor(max_workers=4) as executor:
        for area in selected_areas:
            for time in selected_times:
                time = int(time)
                area = int(area)
                date = int(date)
                executor.submit(get_balance_badminton, area, time, date)


def create_gui():
    root = tk.Tk()
    root.title("羽毛球")

    tk.Label(root, text="选择日期 (YYYYMMDD):").grid(row=0, column=0, sticky='w')
    date_entry = tk.Entry(root)
    date_entry.insert(0, int(datetime.now().strftime("%Y%m%d")) + 1)
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
                with open("../PHPSESSID.txt", "w") as f:
                    f.write(new_session_id)
                messagebox.showinfo("成功", "PHPSESSID已更新。")
                global PHPSESSID
                PHPSESSID = new_session_id
            except Exception as e:
                messagebox.showerror("错误", f"无法写入文件: {e}")

    def on_confirm():
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

        run_get_balance_gym(selected_areas, selected_times, date)

    modify_button = tk.Button(root, text="修改PHPSESSID", command=on_modify_phpsessid)
    modify_button.grid(row=8, column=0, pady=10, sticky='w')

    confirm_button = tk.Button(root, text="确认", command=on_confirm)
    confirm_button.grid(row=8, column=1, pady=10, sticky='w')

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


if __name__ == "__main__":
    create_gui()
