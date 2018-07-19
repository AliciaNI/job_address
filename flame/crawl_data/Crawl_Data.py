#coding:utf-8
import re
import lxml
import lxml.etree
import flame.crawl_data.Merge_Url
import flame.crawl_page.GetPageSourceRequest
import threading
'''
遍历所有的链接，从链接中提取
1：工作名称
2：公司名称
3：薪资
4：职位信息
5：上班地址
6：公司信息
'''
class CrawlData:
    def __init__(self,jobname,searchtype, resultqueue):
        self.jobname = jobname
        self.searchtype = searchtype
        self.resultqueue = resultqueue

    def CrawlInformations(self):
        # urllist = flame.crawl_data.Merge_Url.Merge_Url(self.jobname,self.searchtype)
        # geturllist = urllist.merge_url()
        #     AllInformations = []
        while True:
            urlset = yield
            if not urlset:
                break
            thd = threading.Thread(target=self.goData, args=(urlset,))
            thd.start()
            thd.join()
        # for urlset in geturllist:

    def goData(self, urlset):
        # print(urlset, len(urlset))
        for url in urlset:     #获取到所有的链接地址
            thd = threading.Thread(target=self.getData, args=(url, ))
            thd.start()
            thd.join()

    def getData(self, url):
            AllInformations = []
            pagedata = flame.crawl_page.GetPageSourceRequest.GetPageScourceRequest(url, "utf-8")  # 获取网页源码
            pagedata = pagedata.getpagesource()     #得到网页源码

            mytree = lxml.etree.HTML(pagedata)  # 编码
            WorkName = mytree.xpath("//*[@class='cn']/h1/@title")  # 1：工作名称
            CompanyZone = mytree.xpath("//*[@class='cn']/span/text()")  # 7:地区
            CompanyName = mytree.xpath("//*[@class='cname']/a/@title")  # 2：公司名称
            Salary = mytree.xpath("//*[@class='cn']/strong/text()")  # 3：薪资
            JobInformation = mytree.xpath("//*[@class='bmsg job_msg inbox']/text()")  # 4：职位信息
            if ''.join(JobInformation).strip() == '':
                JobInformation = mytree.xpath("//*[@class='bmsg job_msg inbox']/p/text()")  # 4：职位信息
            try:
                WorkAddress = mytree.xpath("//*[@class='bmsg inbox']/p/text()")[1] # 5：上班地址
            except:
                WorkAddress=[]
            CompanyInformation = mytree.xpath("//*[@class='tmsg inbox']/text()")  # 6：公司信息
            Release_time = mytree.xpath("//*[@class='t1']/span[@class='sp4'][last()]/text()") # 8：发布日期
            Release_time = Release_time[0][:-2]
            AllInformations.append(WorkName)
            AllInformations.append(CompanyName)
            AllInformations.append(CompanyZone)
            AllInformations.append(Salary)
            AllInformations.append(WorkAddress)
            AllInformations.append(JobInformation)
            AllInformations.append(CompanyInformation)
            AllInformations.append(Release_time)
            # try:
            #     print(AllInformations)  # 输出编码错误
            # except:
            #     pass
            for data in AllInformations:
                # print(data)
                if len(data) == 0:
                    break
            else:
                self.resultqueue.put(AllInformations)
                # print("所有信息获取完毕")
            # return  AllInformations

# import queue
# dataqueue = queue.Queue()
# get = CrawlData('python','51-job', dataqueue)
# # get.CrawlInformations()
# get.getData('http://jobs.51job.com/beijing-cyq/99836378.html?s=01&t=0')