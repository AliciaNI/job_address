# job_address




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
