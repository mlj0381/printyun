# 自助云打印
&nbsp;&nbsp;&nbsp;&nbsp;现在的打印店，特别是学校的打印店普遍遇到的问题就是，顾客拿着U盘或者手机去打印店打印东西，需要先将东西传到打印店的电脑上才能打印，如果人多的情况下就需要排队。那么现在有一个网站顾客可以通过手机或者电脑提前将文件上传，然后选择打印份数、黑白参数、横/纵后，在线通过微信/支付宝付款，系统返回给一个订单号，打印店的打印机自动根据这些信息打印，顾客拿着订单号到店直接取文件就可以解决很多麻烦的事情。  
  自助云打印系统就是为了解决这个问题而诞生的。  
  系统刚在起步阶段，目前已经可用，有如下功能：  
  1、支持电脑/手机远程上传文件  
  2、支持pdf、word、excel、ppt等常见打印文件  
  3、支持微信/支付宝支付（需要自行开通相应服务，或者使用第三方）  
  4、支付是否排版，考虑到打印样式繁多，如果选择需要排版，可先上传文件到服务器，顾客去打印店后告知老板打印要求，老板再通过系统直接打印，避免了U盘传输等。  
  5、老板可后台查看所有历史订单及需要排版的订单，可以在线预览/下载打印等  
## 说明
此开源版本仅仅是把资料上传系统，如果需要自动打印还需要一个系统去监控数据库进行打印，此系统日后开源。  

  **作业流程图**
![](http://pic.printyun.cn/printyun_overflow.png)
  ---
  在线测试地址：  
  http://139.9.7.123:8001/login/login   
  测试账号：123456  密码：123456  
  因为测试地址未安装redis，所以无法测试支付，实际环境已经测试可用，需要自行配置
  ---

## 部署
因为系统本身业务比较复杂，里面需要修改的地方比较多，有能力的朋友可以根据debug修改，这里提供需要修改的文件，仅供参考:  
app/certs 三个密钥文件  
app/config.py 数据库配置  
app/sms.py 阿里sms相关配置  

### 1、本机测试  
修改完上述位置配置后  
```python
pip install -r requirements.txt
flask run 
python worker.py  #再开一个shell执行此命令，如果不使用支付系统则可以不开启
```  
### 2、Docker部署  
上述配置修改好后  
```
docker image build -it printyun .
docker container run -d -p 8001:8001 --name printyun pringyun
```
宿主主机打开http://127.0.0.1:8001 看到hello world成功  

## 相关URL
/login/login 登录  

## 部分截图
![](http://pic.printyun.cn/printyun1.png)
![](http://pic.printyun.cn/printyun2.png)
![](http://pic.printyun.cn/printyun3.png)










