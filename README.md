# HeraldWebService


## 项目部署

> 该部分仅介绍在`Unix-like`系统下的部署, `Windows`上部署请自行参考

```bash
virtualenv2 venv                    # 新建venv的Python环境, 部署时只需新建一次
source venv/bin/activate            # 使用新建的Python环境, 每次启动项目时必须
pip install -r requirements.txt     # 安装依赖

cp mod/models/mysql/db.py.example mod/models/mysql/db.py # 数据库配置
python main.py
```


## 不同请求分类

### 不需要缓存, 直接请求

* AuthHandler
* term
* sidebar
* curriculum
* pe
* simsimi
* library_hot
* renew
* search
* pc
* jwc
* schoolbus
* user
* query
* room
* tice
* yuyue

### 从缓存中读取

* card
* exam
* gpa
* lecture
* library
* nic
* pedetail
* phyLab
* room
* srtp

### 未添加
* week
* lecturenotice


## 项目构成情况

### 本项目为两个子项目所组成

* `WebService`是所有项目的统一接口, 

* `WebCrawler`是分布式爬虫的管理项目, 通过此来分发请求

>   两个项目原属于不同的项目, 但是考虑到两者有较多的相似, 
> 许多的模块代码需要复用, 两者也必须同时启动.

>   两个项目合并后, 最需要考虑的便是两者的日志记录的不同.
> `WebService`的日志记录是一直会产生的, 而`WebCrawler`的日志一般为报错信息

> 因此, `WebService`中的标准日志记录将会定向到标准输出中, 
> 而两者中的错误日志将保存在文件`webservice_error.log`中

### 项目的结合方式

`WebService`为`tornado`服务程序, `WebCrawler`程序为简单的分发处理程序

这里的两个项目应当分属两个线程, 两者的除了队列交流外, 没有耦合. 

> 请求队列我们采用了已经封装好的`redis`队列, 

> 注意: 两个项目的结合与队列的选择完全无关, 
> 仅仅是由于两个项目中重复的模块代码十分多, 故而将两个项目结合, 
> 请读者不要臆想

