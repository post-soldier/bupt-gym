自动抢北邮本部羽毛球场，体育馆脚本。

如何使用：

  1.安装运行所需环境，在根目录下，运行 pip install -r requirements.txt
  
  2.手动获取所需参数：
  
    (1)下载一个抓包软件，这里就以国产的Reqable举例，如何配置就不再此进行说明了，B站上有教程
    
    (2)登录微信，运行抓包软件，进入联系人-北京邮电大学-体育馆预约,随便点几下
    
    (3)停止抓包，找到包含“reservation.bupt.edu.cn”的请求，在请求头里找到Cookie，里面有一段“PHPSESSID=xxxxxx”,xxxxxxx就是我们要抓取的数据，记下来(每天都会变，每次都需要重新获取)
    
  3.将获取到的参数放在PHPSESSID.txt文件中
  
  4.打开badminton.py,找到最下面的“get_balance_badminton(1,9,20180205)”的函数调用，这是我们抢场的函数
  
  ![image](https://github.com/post-soldier/bupt-gym/assets/165042370/71971fe7-ddbe-4ae4-804d-d1823757062b)

  5.第一个参数是羽毛球场编号，如要预定“羽毛球场1号”，则id=1
  
    第二个参数是时间段，在time.txt中查表得到，如要预定“15:00-16:00"时间段的场，则time=9
    
    第三个参数是要预定的日期，date=“20180205”表明要预约2018年2月5号的场次
    
  6.运行，开始抢场
  


  注意事项：
  
    1.本程序是死循环，抢到场后请手动暂停
    
    2.如果出现“requests.exceptions.ProxyError: HTTPSConnectionPool”类型的错误，可能是因为抓包软件没有关闭导致的，请关闭后重试


  求助：
    本程序也是可以抢健身房的，但是在进入付款界面的时候有腾讯的滑块检测，有没有大佬知道怎么直接使用js逆向破解的，求教。
    
    在网上找到4篇文章，也看不懂，希望有看得懂的大佬能指点一下。
    
    https://www.52pojie.cn/thread-1521480-1-1.html
    
    https://mp.weixin.qq.com/s/C8gB-D6EUliPXoMgjk0Bag
    
    https://mp.weixin.qq.com/s/EmwuL3ToKwDFwCILZTM1AQ
    
    https://blog.csdn.net/weixin_43411585/article/details/123810961


    
