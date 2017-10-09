# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json
import threading
import queue
import urllib
import urllib.request

# 登录退出
from django.contrib import auth
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

from django.db import connection
from django.shortcuts import render, HttpResponse, HttpResponseRedirect
from django.http import JsonResponse

# 提数据
import flame.crawl_data.Merge_Url
# 数据库
from . import models

# 数据保存队列， 传数据去界面
to_url_queue = queue.Queue()
# 地区队列
zone = ['延庆', '怀柔', '密云', '昌平', '顺义', '平谷', '门头沟', '海淀', '朝阳', '丰台', '石景山', '房山', '大兴', '通州']


# Create your views here.

# 404 自定义404错误页
def page_not_found(request):
    return render(request, '404.html')


# 建表
def createtable(tablename):
    try:
        cursor = connection.cursor()
        # tablename = 'job_url'
        sql = """CREATE TABLE """ + tablename + """(id INT NOT NULL auto_increment PRIMARY KEY,
                company VARCHAR (50) NOT NULL,
                salary VARCHAR(50) NOT NULL,
                job VARCHAR(50) NOT NULL,
                job_information VARCHAR(5000),
                company_information VARCHAR(5000),
                company_zone VARCHAR(20),
                zone_code INT(10),
                address VARCHAR(200) NOT NULL,
                lng DECIMAL(20, 15) NOT NULL,
                lat DECIMAL(20, 15) NOT NULL
                )
            """
        cursor.execute(sql)
        return True
    except Exception as e:
        print(str(e))
        return False


# 登录
def login(request):
    if request.method == 'POST':
        # 获取输入
        username = request.POST.get('username', None)
        password = request.POST.get('password', None)
        if username and password:
            # 验证数据库中是否存在，成功则返回用户对象，否则返回NONE
            user = auth.authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:  # 账号已激活
                    # 登录
                    auth.login(request, user)
                    return HttpResponseRedirect('/flame/search')
                else:
                    return render(request, 'flame/login.html', {'error': '用户已冻结'})
            else:
                return render(request, 'flame/login.html', {'error': '用户名或密码错误'})
        else:
            return render(request, 'flame/login.html', {'error': '请输入用户名或密码'})
    else:
        return render(request, 'flame/login.html')


# 登出
def logout(request):
    auth.logout(request)
    return HttpResponseRedirect(request, 'flame/login.html')


# 注册
def register(request):
    if request.method == 'GET':
        return render(request, 'flame/register.html')
    elif request.method == 'POST':
        username = request.POST.get('username', None)
        nick = request.POST.get('nick', None)
        password = request.POST.get('password', None)
        repassword = request.POST.get('re_password', None)

        try:
            user = User.objects.get(username=username)
        except:
            user = None

        if user is None:
            if username:
                if password:
                    if repassword:
                        if password == repassword:
                            User_info = {
                                'username': username,
                                'password': make_password(password),
                            }
                            User.objects.create(**User_info)
                            uid = User.objects.get(username=username)
                            user_info = {
                                'nick': nick,
                                'password': make_password(password),
                                'user_id': uid.id,
                            }
                            models.UserProfile.objects.create(**user_info)
                            return HttpResponseRedirect('/flame/login')
                        else:
                            return render(request, 'flame/register.html', {'error': '两次输入的密码不一致'})
                    else:
                        return render(request, 'flame/register.html', {'error': '请输入确认密码'})
                else:
                    return render(request, 'flame/register.html', {'error': '请输入密码'})
            else:
                return render(request, 'flame/register.html', {'error': '请输入用户名'})
        else:
            return render(request, 'flame/register.html', {'error': '用户名已存在'})
    else:
        return render(request, 'flame/login.html')


# 设置
@login_required
def setting(request):
    if request.method == 'GET':
        return render(request, 'flame/setting.html', {'setting': 'active'})
    elif request.method == 'POST':
        everynums = request.POST.get('every_ye_nums')
        req = render(request, 'flame/setting.html', {'setting': 'active', 'ye_num': everynums})
        req.set_cookie('everynums', everynums, max_age=60 * 60 * 24 * 365)
        return req


# 搜索
@login_required
def search(request):
    searchlist = models.urltype.objects.all()
    # if request.method == 'GET':
    return render(request, 'flame/search.html', {'searchtypelist': searchlist, 'search': 'active'})
    # elif request.method == 'POST':
    #     return render(request, 'flame/search.html', {'search': 'active'})


# 展示
@login_required
def show(request):
    # if request.method == 'POST':
    everynums = request.COOKIES.get('everynums', 19)
    # 获取搜索内容和搜索的网址类型
    # jobname = request.POST.get('searchjob', None)
    # searchtype = request.POST.get('searchurl', None)
    # if jobname is None:
    jobname = request.GET.get('searchjob', None)
    searchtype = request.GET.get('searchurl', None)

    jobname = jobname.replace(' ', '_')
    print('job and type', jobname, searchtype)
    # 拼接数据库表名
    tablename = jobname + '_' + searchtype
    print('tablename', tablename)
    # 建数据库表
    flags = createtable(tablename)
    print(flags)

    # 如果表存在，则从表中读数据，若表不存在则去爬取数据，然后加到数据库中
    if not flags:
        print('表已存在， 正在读取数据')
        cursor = connection.cursor()
        select_sql = 'select * from ' + tablename
        cursor.execute(select_sql)
        databaselist = cursor.fetchall()
        # print(len(databaselist))
        # print(type(databaselist))
        # 把读出的数据变成 字典的列表
        datalist = []
        for data in databaselist:
            adict = {}
            adict['company'] = data[1]
            adict['job'] = data[3]
            adict['salary'] = data[2]
            adict['job_infor'] = data[4]
            adict['company_infor'] = data[5]
            adict['address'] = data[-3]
            adict['lng'] = data[-2]
            adict['lat'] = data[-1]
            adict['zone_code'] = data[-4]
            datalist.append(adict)

        # return render(request, 'flame/show.html', {'searchjob': jobname, 'searchurl': searchtype, "datalist": datalist, 'refreshflags':False})
        # return render(request, 'flame/show.html', {"datalist": datalist, 'tablename': tablename, 'everynums': everynums})
        return render(request,'flame/show.html', {"datalist": datalist, 'tablename': tablename, 'everynums': everynums})
    else:
        # 爬取数据
        print('表不存在，正在创建并爬取数据。')
        dataqueue = queue.Queue()  # 定义结果队列
        thd = flame.crawl_data.Merge_Url.Merge_Url(jobname, searchtype, dataqueue)
        thd.start()

        # 保存到数据库表, 多线程去保存
        for i in range(5):
            thd = threading.Thread(target=toTable, args=(tablename, dataqueue))
            thd.start()
        # return render(request, 'flame/show.html', {'searchjob': jobname, 'searchurl': searchtype, 'refreshflags':True})
        return render(request, 'flame/show.html', {'everynums': everynums})


# 把数据插入数据库
def toTable(tablename, dataqueue):
    cursor = connection.cursor()
    delete_sql = 'delete from ' + tablename
    cursor.execute(delete_sql)
    for i in range(10000000000):
        try:
            data = dataqueue.get(timeout=50)
            infor_list = handledata(data)
            try:
                insert_sql = """INSERT INTO """ + tablename + """(company, salary, job, job_information, company_information, company_zone, zone_code, address, lng, lat) VALUES('%s', '%s', '%s', '%s', '%s', '%s', '%d', '%s', '%f', '%f')""" % (
                    infor_list[0], infor_list[1], infor_list[2], infor_list[3], infor_list[4], infor_list[5],
                    infor_list[6],
                    infor_list[7], infor_list[8], infor_list[9])
                cursor.execute(insert_sql)
                # [company, salary, job, job_informations, company_informations, company_zone, zonecode, address, lng, lat]

                infor_dict = {
                    'company': infor_list[0],
                    'job': infor_list[2],
                    'salary': infor_list[1],
                    'job_infor': infor_list[3],
                    'company_infor': infor_list[4],
                    'address': infor_list[7],
                    'lng': infor_list[8],
                    'lat': infor_list[9],
                }
                to_url_queue.put(infor_dict)
            except Exception as e:
                print(str(e))
        except Exception as e:
            print(str(e))


# 处理返回的数据，处理成数据库中个字段类型
def handledata(data):
    company = data[1][0]  # 公司
    try:
        salary = data[3][0]  # 薪水
    except:
        salary = ''
    job = data[0][0]  # 职位
    jobinformations = ''  # 职位信息
    for infor in data[5]:
        jobinformations += infor
    job_informations = jobinformations.strip()
    companyinformations = ''  # 公司信息
    for infor in data[6]:
        companyinformations += infor
    company_informations = companyinformations.strip()
    company_zone = data[2][0]
    zonecode = 0  # 非北京地区的
    if company_zone.find('延庆') != -1:
        zonecode = 1
    elif company_zone.find('怀柔') != -1:
        zonecode = 2
    elif company_zone.find('密云') != -1:
        zonecode = 3
    elif company_zone.find('昌平') != -1:
        zonecode = 4
    elif company_zone.find('顺义') != -1:
        zonecode = 5
    elif company_zone.find('平谷') != -1:
        zonecode = 6
    elif company_zone.find('门头沟') != -1:
        zonecode = 7
    elif company_zone.find('海淀') != -1:
        zonecode = 8
    elif company_zone.find('朝阳') != -1:
        zonecode = 9
    elif company_zone.find('丰台') != -1:
        zonecode = 10
    elif company_zone.find('石景山') != -1:
        zonecode = 11
    elif company_zone.find('房山') != -1:
        zonecode = 12
    elif company_zone.find('大兴') != -1:
        zonecode = 13
    elif company_zone.find('通州') != -1:
        zonecode = 14

    address = data[2][0] + data[4]

    # 解析出地址坐标
    url = 'http://api.map.baidu.com/geocoder/v2/?address='
    # address = request.quote('北京市海淀区上地十街10号')
    address_a = urllib.request.quote(address)
    output = '&output=json&ak='
    ak = 'cQ1m9iXADTf43GBjLBLGaNNMvDkOdpx9'
    # callback = '&callback=showLocation'

    url = url + address_a + output + ak  # + callback   # 拼接网址
    res = urllib.request.urlopen(url).read().decode('utf-8')
    # print(res)
    rez = json.loads(res)
    lng = rez['result']['location']['lng']  # 经度
    lat = rez['result']['location']['lat']  # 纬度
    infor_list = [company, salary, job, job_informations, company_informations, company_zone, zonecode, address, lng,
                  lat]
    # print(infor_list)
    return infor_list

# 传数据去界面
def toUrlData(request):
    if request.method == 'POST':
        datalistb = []
        while not to_url_queue.empty():
            try:
                data = to_url_queue.get()
                # print('kl', type(data), len(data))
                # for k in data.keys():
                #     print('12')
                #     print(k, data[k])
                #     print('124')
                #     try:
                #         data[k] = data[k].decode('utf-8', errors='ignore')
                #     except:
                #         pass
                #     print('1235')
                # print(data)
                datalistb.append(data)
            except:
                pass
        # print('datalist', datalist)
        return JsonResponse(datalistb, safe=False)
    else:
        return HttpResponse(json.dumps({'datalistb': 'error'}))


# 地图
@login_required
def map(request):
    """
    地图
    :param request:
    :return:
    """
    tablename = request.GET.get('tablename', None)
    if tablename is None:
        lng = request.GET.get('lng')
        lat = request.GET.get('lat')
        zonecode = request.GET.get('zonecode')
        address = request.GET.get('address')
        company = request.GET.get('company')
        data = [[lng, lat, zonecode, address, company]]
        data = json.dumps(data)
        return render(request, 'flame/map.html', {'datalist': data})
    else:
        xylist = []
        cursor = connection.cursor()
        select_sql = 'select * from ' + tablename
        cursor.execute(select_sql)
        databaselist = cursor.fetchall()
        for data in databaselist:
            company = data[1]
            job = data[3]
            salary = data[2]
            address = data[-3]
            lng = float(data[-2])
            lat = float(data[-1])
            zone_code = data[-4]
            xylist.append([lng, lat, zone_code, company, job, salary, address])
        return render(request, 'flame/map.html', {'datalist': json.dumps(xylist)})
