>实现了学生，班级的增删改查RestFul API

>实现了按名字查询学生，班级，并使用和维护cache

>使用DRF自动化生成API文档 

>前端可使用交互式API文档调试，时间紧迫，vue页面暂未实现。 

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

## 接口测试(每次运行均会创建3条班级和10条学生数据)
> python manage.py test

如遇报错，详情可用浏览器打开并刷新./error.html查看

## 文档
> http://localhost:8000/docs/


## 缓存设计优点
- cache数据结构解耦拆分> 学生信息, 学生映射，班级学生映射， 班级映射
- 使用str数据类型，无缝迁移redis/memcache等
- cache的value反序列化后为dict/list,更新函数都是幂等操作
- 新增修改皆可使用
