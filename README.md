## Flask框架实现素材下载站接口说明
> 实现的主要功能及说明
- 搜索功能
```
接口地址：/api/search
    
    参数说明：
        @page: 第几页
        @kw: 关键词
        @cat_1: 一级分类
        @cat_2: 二级分类
        @sort: 排序 1=>综合排序 2=>下载量排序 3=>最新排序
    
    
```
*搜索功能使用当前流行的elasticsearch搜索引擎来实现，因为之前的搜索都是用sphinx来做的，也是为了面试和学习因此就利用elasticsearch来实现搜索，发现elasticsearch相比sphinx可以做更多的筛选和搜索算法的定制，功能比sphinx更强大，但是相比于sphinx的文档存储elasticsearch更吃内存。*


- 异步下载功能
```
入下载队列接口：/api/down/<bianhao>
查看任务状态接口：/api/down/status/<task_id>
获取下载结果：/api/down/get-result/<bianhao>
```
*异步下载使用的是celery分布式任务队列，同时也用beanstalkd实现了异步下载。首先后台以守护进程的方式运行worker，当用户请求下载接口时，celery会把这个任务放到消息队列去，消费者会检查该任务有没有被下载过，如果被下载过OSS上会存有相应的资源，直接取回返回给用户，如果没有则会到一个第三方网站模拟登陆后下载原图上传OSS，上传成功后会请求OSS生成一条下载链接并返回，请求get-result接口获取资源*



- 登录登出功能

```
接口地址：/api/login 和 /api/logout

利用oAuth2.0认证实现QQ登入登出的功能
```

- 收藏相关功能
```
获取收藏：/api/user/get_collect
添加收藏：/api/user/add_collect/<int:png_id>
删除收藏：/api/user/del_collect/<int:png_id>

主要利用SQLAlchemy操作数据库来实现
```
- 详情页
```
查看素材详情：/api/detail/<int:png_id>

利用elasticsearch搜索引擎获取素材详细信息
```