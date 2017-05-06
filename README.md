## proxyapi
为sillpool提供Restful api服务。

### 运行
```
python manage.py runserver
```

### 用法
##### 1、获取可用的proxy
```
curl http://localhost:8080/proxy/list/{page}
```
参数
page：限制获取proxy的数量
