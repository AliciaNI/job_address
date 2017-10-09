# job_address
项目介绍：
    这是一个从招聘网站爬职位，显示到网页端的项目。

描述流程：
登录 ==》 搜索界面 ==》 提交搜索内容之后 ==》 调到展示界面 == 数据库有数据 ==》 直接读取数据库展示到界面
                                                          |
                                                           ==  数据库没有  ==》 调用爬虫去爬取，爬到一条，加到数据库
                                                                                                          并展示到界面
函数流程：
login ------ search ----  show ---- show.html -- map.html
  |            |            |
  |            |            |
  register-login            |
                            |
                         调用爬虫
                            |
                         Merge_Url -- handledata  |-- toTable    --| --- show.html  -- map.html
                                                  |-- toUrlData  --|

应用技术：
爬虫：
    selenium, requests, urllib2 爬取界面
    re, lxml, bs4 提取所需数据
    多线程，协程快速爬取网页信息
    分布式，多机器爬取数据

数据库：
    MySql存储数据

后台：
    Django，
        自定义错误页面
        用户的注册登录
        搜索功能
        可配置每页显示几条数据
    bootsrap搭建基本页面
    调用百度地图接口，在百度地图上显示一个或全部公司。
    实现一边爬取数据一边显示到页面
    ajax实现页面局部刷新， 实现分页功能

爬虫中使用yield实现，爬到一条url就爬一条具体内容数据，
view.py 和 爬虫py 内容数据的传递 通过 队列。deque

2017-9-17：
    显示数据：
        两种情况，
            1、一种是，数据库中已有数据，直接读取，计算数据量，实现分页
            2、二种是，数据库没有这个表，要去现爬，
        1、直接从数据库读，转成字典的列表后，传到show.html界面进行处理。
        2、使用ajax定时去后台请求数据。每隔两秒，
            数据爬下来后，保存到数据库的同时，把数据保存到队列中，
            当ajax隔了两秒后，把队列中个东西读走，转成字典的列表， 显示到界面。
            py传数据去界面：
                from django.http import JsonResponse

                def a(request):  // 简略版
                    return JsonResponse(datalistb, safe=False)

2017-9-18:
    实现分页：（重点：获取标签，加标签，加属性，去属性，隐藏显示标签。）
        两种情况，
            1、一种是，数据库中已有数据，直接读取，计算数据量，实现分页
            2、二种是，数据库没有这个表，要去现爬，
        1、① 计算数据量，a
              规定每页显示数据条数， everynums
              a / everynums = c ， 即有多少页
           ② 默认所有数据隐藏， 在shou.html中对应标签加属性 style="display:none;"
              默认显示第一页的    $('tr').slice(1, everynums).removeAttr('style')  // 第0个 为标题
              再给页码加上点击事件，实现点击时显示相应页码的数据
              点击的页码 pagenum
              首先隐藏其他页的，即上一次显示的页的内容
              上一次显示的页码 prepagenum
              $('tr').slice((prepagenum-1)*everynums+1, prepagenums*everynums+1).attr('style', 'display:none')
              再显示这次点击的页码的内容
              $('tr').slice((pagenum-1)*everynums+1, pagenum*everynums+1).removeAttr('style')
        2、① 目标：
                默认显示第一页内容，
                有新内容加到最后，翻页时显示
           ② 先隐藏前面点击的页，再显示这次点击的页，同上， 同一套代码

2017-9-27：
    1、自定义自己的错误页面。
        定制404错误页面。
        ① 在templates文件夹下，新建错误html文件
        ② 修改settings.py
            DEBUG = False
            ALLOWED_HOSTS = ['*']
        ③ 在views.py中写函数
            # 404 自定义404错误页
            def page_not_found(request):
                return render(request, '404.html')
        ④ 在 flame 的urls.py中写：
            handler404 = 'views.page_not_found'

2017-9-28
    1、修改search.html页面，form的提交方式为get，这样刷新show.html时就不会提示是否重新提交表单了。
    2、{% csrf_token %} , 放开'django.middleware.csrf.CsrfViewMiddleware'时，在form表单中添加这句话。就可正常提交post请求了。