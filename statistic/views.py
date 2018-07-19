from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from flame.models import position_website, urltype
import matplotlib.pyplot as plt
import matplotlib
import os
from django.db import connection
from job_address.SendMailBase import SendEmailBase
# Create your views here.

def page_not_found(request):
    return render(request, '404.html')

def draw(data_list, name_list, file_dir):
    matplotlib.rcParams['font.sans-serif'] = ['simhei']
    matplotlib.rcParams['font.family'] = 'sans-serif'
    i = 1
    while True:
        try:
            fig = plt.figure(i)
            break
        except:
            print('- - '*20, i)
            i += 1
    for index, value in enumerate(data_list):
        plt.bar([index], [value], label=name_list[index])
    plt.legend()
    current_dir = os.path.join(os.getcwd(), 'static\statistic\image')
    fig.savefig(os.path.join(current_dir, file_dir))
    fig.clear()
    plt.close()

def sendEmail(img_list):
    content = """
                    <p>Python 邮件发送测试...</p>
                    <p><a href="http://www.runoob.com">菜鸟教程链接</a></p>
                    <p>图片演示：</p>
                    <p><img src="cid:image1"></p>
                """
    subject = '哈哈哈哈6'
    a = SendEmailBase('smtp.163.com', 25, 'yincheng8848@163.com', 'tsinghua8848', ['yincheng8848@163.com'], subject)  # 初始化类
    a.setMessage(content, 'html', 'utf-8')  # 正文
    for img in img_list:
        a.setContentImage(img, 'image1')  # 设置正文图片
        # a.setEnclosure(r'E:\li-note\spy.ini', 'spy.ini')    # 附件
        a.setImageEnclosure(img, 'mouse.jpg') # 图片附件
    a.sendEmail()  # 发送

@login_required
def analysis(request):
    table_name_list = position_website.objects.all().values_list('position', 'website_id__nick', 'count')
    print(table_name_list)
    data_list = []
    name_list = []
    table_list = []

    # 职位数量
    # fig1 = plt.figure()
    for i in table_name_list:
        name_list.append(i[0])
        table_list.append('_'.join(i[:2]))
        data_list.append(i[2])
    draw(data_list, name_list, 'position_number/1.jpg')

    # 日期数量
    cursor = connection.cursor()
    cursor.execute('select count(*), release_time from python_51job group by release_time')
    res_group_release = cursor.fetchall()
    print(res_group_release)
    data_list = []
    name_list = []
    for i in res_group_release:
        data_list.append(i[0])
        name_list.append(i[1])
    draw(data_list, name_list, 'date_number/1.jpg')

    # 薪水数量
    cursor.execute('select count(*), salary from python_51job where salary_range>0 group by salary_range')
    res_group_release = cursor.fetchall()
    print(res_group_release)
    data_list = []
    name_list = []
    for i in res_group_release:
        data_list.append(i[0])
        name_list.append(i[1])
    draw(data_list, name_list, 'salary_number/1.jpg')

    img_list = []
    current_dir = os.path.join(os.getcwd(), 'static\statistic\image')
    img_list.append(os.path.join(current_dir, 'position_number/1.jpg'))
    img_list.append(os.path.join(current_dir, 'date_number/1.jpg'))
    img_list.append(os.path.join(current_dir, 'salary_number/1.jpg'))
    sendEmail(img_list)
    position_image_list = {
        'image_list_length': 1,
        'dirname': ['/static/statistic/image/position_number/1.jpg'],
    }
    date_image_list = {
        'image_list_length': 1,
        'dirname': ['/static/statistic/image/date_number/1.jpg'],
    }
    salary_image_list = {
        'image_list_length': 1,
        'dirname': ['/static/statistic/image/salary_number/1.jpg'],
    }
    return render(request, 'statistic/analysis.html', {'position_image_list': position_image_list, 'date_image_list': date_image_list, 'salary_image_list': salary_image_list})