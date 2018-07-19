#coding:utf8
__author__ = 'Li'
'''
发邮件类：
    支持发纯文本，
    支持发附件，
    支持发图片附件，
    支持发文本图片，
    （纯文本 和 文本图片 不可同时有）
    setContentImage 函数可以用 setImageEnclosure  代替  (有时不行)
'''

import smtplib
from email.mime.text import MIMEText
from email.header import Header
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage


class SendEmailBase:
    def __init__(self, server, port, sender, password, receivers, subject):
        """
        :param server:      # 服务：smtp.163.com。。。。
        :param port:        # 端口： 25.。。。
        :param sender:      # 发送人邮箱
        :param password:    # 密码
        :param receivers:   # 接收人邮箱列表
        :param subject:     # 邮件标题
        """

        self.server = server
        self.port = port
        self.sender = sender
        self.password = password
        self.receivers = receivers
        self.subject = subject

        self.imageid = 0

        # 初始化附件
        self.message = MIMEMultipart('related')
        self.msgAlternative = MIMEMultipart('alternative')
        self.message.attach(self.msgAlternative)

        # 初始化From，To， Subject
        self.message['From'] = Header(self.sender, 'utf-8')
        self.message['To'] = self.receivers[0]
        self.message['Subject'] = Header(self.subject, 'utf-8')

    # 邮件正文
    def setMessage(self, content, textformat, code):
        """
        :param content:         # 文本内容
        :param textformat:      # 文本格式  'plain', 'html' .....
        :param code:            # 编码  'utf-8'....
        :return:
        """
        self.msgAlternative.attach(MIMEText(content, textformat, code))

    # 设置带图片的正文中的图片
    def setContentImage(self, imagefilepath, imageid):
        """
        :param imagefilepath:  # 图片路径
        :param imageid:        # 图片编号 image1, image2  字符串
        :return:
        """
        fp = open(imagefilepath, 'rb')
        msgImage1 = MIMEImage(fp.read())
        fp.close()
        # msgImage1.add_header('Content-ID', '<' + imageid + '>')  # 也可以
        msgImage1.add_header('Content-ID', imageid)
        self.message.attach(msgImage1)

    # 上传附件
    def setEnclosure(self, filepath, showname):
        """

        :param filepath:  # 附件路径
        :param showname:  # 附件显示的名字
        :return:
        """
        attachbase = MIMEText(open(filepath, 'rb').read())
        attachbase['Content-type'] = 'application/octer-stream'
        attachbase['Content-Disposition'] = 'attachment; filename= %s' % showname
        self.message.attach(attachbase)

    # 上传图片附件
    def setImageEnclosure(self, imagefilepath, imagename):
        """

        :param imagefilepath:   # 图片附件的路径
        :param imagename:       # 图片附件的显示名字
        :return:
        """
        fp = open(imagefilepath, 'rb')
        msgImage1 = MIMEImage(fp.read())
        fp.close()
        # msgImage1.add_header('Content-ID', imagename)
        msgImage1.add_header('Content-Disposition', 'inline; filename=%s' % imagename)
        self.message.attach(msgImage1)

    # 发送邮件
    def sendEmail(self):
        try:
            self.smtpObj = smtplib.SMTP()
            self.smtpObj.connect(self.server, self.port)
            self.smtpObj.login(self.sender, self.password)
            self.smtpObj.sendmail(self.sender,
                                  self.receivers,
                                  self.message.as_string())
            print('邮件发送成功。')
        except Exception as e:
            print('发送失败。', str(e))

    def __del__(self):
        self.smtpObj.close()
# #
# if __name__ == '__main__':
#     content = """
#                 <p>Python 邮件发送测试...</p>
#                 <p><a href="http://www.runoob.com">菜鸟教程链接</a></p>
#                 <p>图片演示：</p>
#                 <p><img src="cid:image1"></p>
#             """
#     subject = '哈哈哈哈6'
#     a = SendEmailBase('smtp.163.com', 25, 'yincheng8848@163.com', 'tsinghua8848', ['yincheng8848@163.com'], subject)  # 初始化类
#     # a = SendEmailBase('smtp.163.com', 25, 'alicia_n@163.com', 'alicia_n163', ['yincheng8848@163.com'], subject)  # 初始化类
#     a.setMessage(content, 'html', 'utf-8')  # 正文
#     a.setContentImage(r'C:\Users\DAO\Desktop\dou_image\2012111222351533.jpg', 'image1')  # 设置正文图片
#     a.setEnclosure(r'E:\li-note\spy.ini', 'spy.ini')    # 附件
#     a.setImageEnclosure(r'C:\Users\DAO\Desktop\dou_image\2012111222463057.jpg', 'mouse.jpg') # 图片附件
#     a.setImageEnclosure(r'C:\Users\DAO\Desktop\dou_image\mao_.png', 'maomi.png')  # 图片附件
#     a.sendEmail()  # 发送