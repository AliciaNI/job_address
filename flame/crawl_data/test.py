#coding:utf-8

import re
import lxml
import lxml.etree
import flame.crawl_page.GetPageSourceRequest
'''
遍历所有的链接，从链接中提取
1：工作名称
2：公司名称
3：薪资
4：职位信息
5：上班地址
6：公司信息
7:地区
'''
url ="http://jobs.51job.com/beijing-cpq/93944621.html?s=01&t=0"
page = flame.crawl_page.GetPageSourceRequest.GetPageScourceRequest(url,'utf-8')
source = page.getpagesource()
mytree = lxml.etree.HTML(source)  # 编码
WorkName = mytree.xpath("//*[@class='cn']/h1/@title")  #1：工作名称
CompanyZone = mytree.xpath("//*[@class='cn']/span/text()")  #7:地区
CompanyName = mytree.xpath("//*[@class='cname']/a/@title")  #2：公司名称
Salary = mytree.xpath("//*[@class='cn']/strong/text()")#3：薪资
JobInformation = mytree.xpath("//*[@class='bmsg job_msg inbox']/text()")#4：职位信息
WorkAddress = mytree.xpath("//*[@class='fp']/text()")[1]#5：上班地址
CompanyInformation=mytree.xpath("//*[@class='tmsg inbox']/text()")#6：公司信息
print(WorkAddress)
print(WorkName[0],CompanyZone[0],CompanyName[0],Salary[0],JobInformation,WorkAddress,CompanyInformation)