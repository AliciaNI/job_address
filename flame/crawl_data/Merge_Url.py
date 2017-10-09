# coding:utf-8
import re
import queue
import lxml.etree
import lxml
import urllib.request
import threading

import flame.crawl_data.Crawl_Data
import flame.crawl_page.GetDataFromFunc_xpath
import flame.crawl_page.GetPageSourceRequest

'''
拼接url搜索框内容
http://search.51job.com/list/010000,000000,0000,00,9,99,+name+,2,+数值+.html?lang=c&stype=1&postchannel=0000&workyear=99&cotype=99&degreefrom=99&jobterm=99&companysize=99&lonlat=0%2C0&radius=-1&ord_field=0&confirmdate=9&fromType=1&dibiaoid=0&address=&line=&specialarea=00&from=&welfare=
'''


class Merge_Url(threading.Thread):
    def __init__(self, jobname, searchtype, dataqueue):
        super(Merge_Url, self).__init__()
        self.jobname = jobname
        self.searchtype = searchtype
        self.generator_crawl_data = flame.crawl_data.Crawl_Data.CrawlData(self.jobname, self.searchtype, dataqueue).CrawlInformations()
        next(self.generator_crawl_data)

    def run(self):
        if self.searchtype == '51job':
            jobname = urllib.request.quote(self.jobname)
            pagecontent = []  # 保存所有的工作岗位链接
            searchurl = "http://search.51job.com/jobsearch/search_result.php?fromJs=1&jobarea=010000&keyword=" + jobname + "&keywordtype=2&lang=c&stype=2&postchannel=0000&fromType=1&confirmdate=9"

            page = flame.crawl_page.GetDataFromFunc_xpath.GetUrl(searchurl, "utf-8")  # 获取第一页开始的每页的工作链接
            pageco = page.get_51job()   # 得到的是 页面中所有的职位链接
            self.generator_crawl_data.send(pageco)     # send
            pagecontent.append(pageco)
            # print(pagecontent)
            pagedata = flame.crawl_page.GetPageSourceRequest.GetPageScourceRequest(searchurl, "utf-8")  # 获取网页源码
            pagedata = pagedata.getpagesource()

            # print(pagedata)       #打印网页源码
            mytree = lxml.etree.HTML(pagedata)  # 编码
            pagenum = mytree.xpath("//*[@class = 'td']/text()")  # ['共111页，到第', '页']
            # print(pagenum)
            # print(pagenum[0])  # 共111页，到第
            pag = re.compile(r"(\d+)", re.IGNORECASE)
            pagenumber = pag.findall(pagenum[0])
            pagenumber = eval(pagenumber[0])  # 111 <class 'int'>
            # print(pagenumber, type(pagenumber))


            for i in range(2, pagenumber + 1):
                searchurl = "http://search.51job.com/list/010000,000000,0000,00,9,99," + jobname + ",2," + str(
                    i) + ".html?lang=c&stype=1&postchannel=0000&workyear=99&cotype=99&degreefrom=99&jobterm=99&companysize=99&lonlat=0%2C0&radius=-1&ord_field=0&confirmdate=9&fromType=1&dibiaoid=0&address=&line=&specialarea=00&from=&welfare="
                page = flame.crawl_page.GetDataFromFunc_xpath.GetUrl(searchurl, "utf-8")  # 获取第二页开始的每页的工作链接
                pageco = page.get_51job()
                self.generator_crawl_data.send(pageco)
                # print('00000000000000000',i,searchurl,type(searchurl))
                pagecontent.append(pageco)  # 将每页的url添加到集合里
                # print(pagecontent)
            self.generator_crawl_data.send('')
            print("获取链接成功")
            # return pagecontent
        elif self.searchtype == 'zhilian':
            pass
        elif self.searchtype == '51cto':
            pass
        else:
            pass


# '''
q = queue.Queue()
page=Merge_Url('python','51-job', q)
page.start()

# '''
