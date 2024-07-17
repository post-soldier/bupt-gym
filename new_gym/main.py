import re
import tkinter as tk
from tkinter import simpledialog, messagebox, ttk
from datetime import datetime
import requests

import slider_verify.TecentSliderVerify

with open("../PHPSESSID.txt", "r") as f1:
    PHPSESSID = f1.read()


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


def pay(time_id, ticket, valid_value):
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
           f'form-data; name=\"total_amount\"\r\n\r\n16\r\n------WebKitFormBoundary1FOdTJeAgQAaYSJ0\r\nContent' \
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


    while datetime.now().strftime("%H") != '12':
        pass

    while int(datetime.now().strftime("%S")) < 1:
        pass

    response = requests.post(url, headers=headers, data=data, cookies=cookie)

    if "北邮体育馆" in response.text:
        print("success")
        return 1
    elif "400 Bad Request" in response.text:
        print("可能抢到了，去订单页看看")
        return 2
    else:
        print(response.text)
        return 0


def get_balance_gym(time, date):
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
        'finall_price': '0',
        'occupy_quota': '1',
    }

    response = requests.post(
        'https://reservation.bupt.edu.cn/index.php/Wechat/MixedPayment/get_balance_and_packages_of_one_user',
        cookies=cookies,
        headers=headers,
        data=data,
    )
    valid_value, is_captcha = get_valid_value("5985", "15415", str(date) + time, str(date))

    print(valid_value)
    print(is_captcha)

    if is_captcha == '0':
        return pay(str(date) + time, "", valid_value)
    else:
        ticket = slider_verify.TecentSliderVerify.slider()
        return pay(str(date) + time, ticket, valid_value)



# get_balance_gym(4, 20240711)


def update_session_id():
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


def run_get_balance_gym():
    global PHPSESSID
    with open("../PHPSESSID.txt", "r") as f1:
        PHPSESSID = f1.read()
    try:
        session_time = int(time_combobox.get().split(': ')[0])
        date = int(date_entry.get())  # Get the input date
        if session_time and date:
            messagebox.showinfo("提示", "显示未响应是正常的，请不要进行任何操作（包括移动鼠标）\n        点击确定开始")
            re = get_balance_gym(session_time, date)
            if re == 1:
                messagebox.showinfo("成功", "成功抢到，请及时进入详情页支付！")
            elif re == 2:
                messagebox.showinfo("??", "可能抢到，请进入详情页查看！")
            else:
                messagebox.showinfo("失败", "对不起，没抢到。")
        else:
            messagebox.showwarning("警告", "请确保日期和场次都已填写。")
    except Exception as e:
        messagebox.showerror("错误", str(e))


def center_window(width=300, height=200):
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
center_window(300, 250)

# Button to update PHPSESSID
update_button = tk.Button(root, text="更新 PHPSESSID", command=update_session_id)
update_button.pack(pady=(10, 5))

# Add a label for instructions
instruction_label1 = tk.Label(root, text="请输入日期（格式：YYYYMMDD）：")
instruction_label1.pack(pady=(10, 5))

# Entry for date
date_entry = tk.Entry(root)
date_entry.insert(0, str(int(datetime.now().strftime("%Y%m%d"))+1))
date_entry.pack(pady=5)

instruction_label2 = tk.Label(root, text="选择时间段：")
instruction_label2.pack(pady=(10, 5))

# Combobox for time slots
time_slots = {
    "2": "08:00-09:00",
    "3": "09:00-10:00",
    "4": "10:00-11:00",
    "5": "11:00-12:00",
    "8": "12:00-13:00",
    "9": "13:00-14:00",
    "10": "14:00-15:00",
    "12": "15:00-16:00",
    "13": "16:00-17:00",
    "15": "17:00-18:00",
    "16": "18:00-19:00",
    "17": "19:00-20:00",
    "18": "20:00-21:00",
    "19": "21:00-22:00"
}
time_combobox = ttk.Combobox(root, values=[f"{k}: {v}" for k, v in time_slots.items()])
time_combobox.pack(pady=5)

# Button to run get_balance_gym
run_button = tk.Button(root, text="开抢", command=run_get_balance_gym)
run_button.pack(pady=(5, 10))

# Start the GUI
root.mainloop()
