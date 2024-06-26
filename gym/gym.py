import requests
import execjs

from datetime import datetime

with open("../PHPSESSID.txt", "r") as f1:
    PHPSESSID = f1.read()

with open("ticket.txt", "r") as f:
    ticket = f.read()

def get_balance_gym(time, date):
    # id是羽毛球场编号，如要预定“羽毛球场1号”，则id=1
    # time是时间段，在time.txt中查表得到，如要预定“08:00-09:00"时间段的场，则time=1
    # date是要预定的日期，date=“20180205”表明要预约2018年2月5号的场次
    cookies = {
        'PHPSESSID': PHPSESSID,
        'think_language': 'zh-cn',
    }
    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'accept-language': 'zh-CN,zh;q=0.9',
        'cache-control': 'no-cache',
        'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'origin': 'https://reservation.bupt.edu.cn',
        'pragma': 'no-cache',
        'priority': 'u=1, i',
        'referer': 'https://reservation.bupt.edu.cn/index.php/Wechat/Show/user',
        'sec-ch-ua': '"Chromium";v="124", "Google Chrome";v="124", "Not-A.Brand";v="99"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'document',
        'sec-fetch-site': 'none',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36 NetType/WIFI MicroMessenger/7.0.20.1781(0x6700143B) WindowsWechat(0x6309092b) XWEB/9079 Flue',
        'x-requested-with': 'XMLHttpRequest',
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

    with open("main_gym.js", "r", encoding="utf-8") as f:
        js = f.read()

    ctx = execjs.compile(js)
    while datetime.now().strftime("%H") != 12:
        pass
    print(1)
    ctx.call("main", PHPSESSID,str(date) + time, ticket)

#example
get_balance_gym(2,20240622)
