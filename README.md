自动抢北邮本部羽毛球场，体育馆脚本。

强烈推荐使用release中的打包好的文件运行

推荐结合指导视频食用：

https://b23.tv/Kx0TOKa

如何使用：

  1.下载对应的release，包括健身房和羽毛球场(new_gym.zip & new_badminton.zip)
  
  2.需要selenium驱动，请使用谷歌浏览器（没有的话先安装）
  
    (1) 下载谷歌浏览器，查看版本（右上角三个点-设置-左侧边栏最下的关于Chrome）
    
    (2) 打开https://googlechromelabs.github.io/chrome-for-testing/known-good-versions-with-downloads.json查看对应版本的驱动下载地址
    
    (3) Ctrl + F查找对应版本的驱动（版本不需要完全相同，前三位版本号一样即可）
    
    (4) 下载结尾为"chromedriver-win64.zip"的文件，一定要是driver
    
    (5) 解压，里面应该只有两三个文件，其中有一个是"chromedriver.exe",复制这个到程序路径下，替换掉自带的chromedriver.exe
    
        
  3.手动获取所需参数：
  
    (1)下载一个抓包软件，这里就以国产的Reqable举例，如何配置就不再此进行说明了，B站上有教程
    
    (2)登录微信，运行抓包软件，进入联系人-北京邮电大学-体育馆预约,随便点几下
    
    (3)停止抓包，找到包含“reservation.bupt.edu.cn”的请求，在请求头里找到Cookie，里面有一段“PHPSESSID=xxxxxx”,xxxxxxx就是我们要抓取的数据，记下来(每天都会变，每天都需要重新获取)
    
  4.将获取到的参数放在PHPSESSID.txt文件中或者在可视化界面修改

  5.解压下载的压缩包，打开main.exe

  6.运行时不要乱动鼠标，以免影响自动程序过滑块验证
  
  7.健身房抢成功会有弹窗提醒，羽毛球抢成功会在命令行出现“success”

  8.成功后尽快进入预约列表进行支付

  9.捡漏模式的日期请在首页进行需改

  10.推送服务配置：
  
    (1)关注『方糖』微信公众号
    
    (2)进入『服务入口』-『Server酱新官网』
    
    (3)在网页上方选择『Key&API』，获取『SendKey』
    
    (4)复制到SendKey.txt里
    
    (5)成功捡漏后会微信通知

  
  注意事项：
  
    1.如果滑块验证出现请求太频繁，可以试着开手机热点或者挂梯子
    
    2.如果出现“requests.exceptions.ProxyError: HTTPSConnectionPool”类型的错误，可能是因为抓包软件或者梯子没有关闭导致的，请关闭系统代理

    

