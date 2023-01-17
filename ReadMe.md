# 环境搭建
- python 国内镜像https://mirrors.huaweicloud.com/python/3.10.0/
- pip3 install numpy -i https://pypi.tuna.tsinghua.edu.cn/simple
- redis官方不支持windows,改用Memcached https://redis.io/docs/getting-started/installation/install-redis-on-windows/
"D:\mydata\full_data\memcached-1.4.5-amd64\memcached-amd64\memcached.exe"
- mysql安装很重，先用内存数据库
- django C:\Users\Thomas\AppData\Local\Packages\PythonSoftwareFoundation.Python.3.10_qbz5n2kfra8p0\LocalCache\local-packages\Python310\site-packages

C:\Users\Thomas\AppData\Local\Programs\Python\Python310
- node.js
- - nmp
# 插件安裝
# 后端代码编写
## 公共库缓存
# 前端代码编写
# 启动脚本
# 自测用例

# 运行
## 安装依赖
### 后端
> pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
## 修改DB和缓存配置
## 初始化DB
> python manage.py makemigrations

> python manage.py migrate
## 初始化数据
> python manage.py createsuperuser

 注意!，windows环境需要在CMD中执行，否则报错

> Superuser creation skipped due to not running in a TTY. You can run `manage.py createsuperuser` in your project to create one manually

## 接口测试
> python manage.py test