自动抢北邮本部羽毛球场，体育馆脚本。

如何使用：

  1.安装运行所需环境，在根目录下，运行 pip install -r requirements.txt
  
    1.1 需要selenium驱动，我传了一个谷歌的，如果不能用请百度selenuim安装，并在TencentSliderVerify.py中的第91行修改对应驱动的地址

  2.手动获取所需参数：
  
    (1)下载一个抓包软件，这里就以国产的Reqable举例，如何配置就不再此进行说明了，B站上有教程
    
    (2)登录微信，运行抓包软件，进入联系人-北京邮电大学-体育馆预约,随便点几下
    
    (3)停止抓包，找到包含“reservation.bupt.edu.cn”的请求，在请求头里找到Cookie，里面有一段“PHPSESSID=xxxxxx”,xxxxxxx就是我们要抓取的数据，记下来(每天都会变，每天都需要重新获取)
    
  3.将获取到的参数放在PHPSESSID.txt文件中或者在可视化界面修改

  4.选择对应的程序运行，健身房或者羽毛球

     健身房：需要设置两个参数，第一个是日期（一般是当天的后一天，会自动填写，如有特殊需求再修改）
     羽毛球场：需要设置三个参数，第一个是日期(同上)，第二个是场号(共九个，可多选)，第三个是时间段（可多选），别选太多，要不容易失败

  5.修改好参数就可以运行了，大概提前一分钟开始，因为过滑块验证需要时间

  6.运行时不要乱动鼠标，以免影响自动程序过滑块验证
  
  7.健身房抢成功会有弹窗提醒，羽毛球抢成功会在命令行出现“success”

  8.可选两种支付方式，余额和微信支付。微信支付需要抢完后进入订单界面完成支付
  


  注意事项：
  
    1.如果滑块验证出现请求太频繁，可以试着开手机热点或者挂梯子
    
    2.如果出现“requests.exceptions.ProxyError: HTTPSConnectionPool”类型的错误，可能是因为抓包软件或者梯子没有关闭导致的，请关闭系统代理

    3.如要使用余额支付，请在主程序代码里搜索“mixed_payment_type”,将后面的wechat_pay更换成"balance_pay"
