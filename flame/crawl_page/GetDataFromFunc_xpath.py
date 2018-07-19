# coding:utf-8
import lxml
import lxml.etree
import flame.crawl_page.GetPageSourceRequest
import re

"""
1:读取网页第一页源码的所有职位链接

"""
class GetUrl(flame.crawl_page.GetPageSourceRequest.GetPageScourceRequest):
    def __init__(self,url,decodetype):
        super(GetUrl, self).__init__(url,decodetype)

    def get_51job(self):
        urlset = set()     #链接集合
        # print(pagedata)

        pagedata = flame.crawl_page.GetPageSourceRequest.GetPageScourceRequest.getpagesource(self)
        mytree = lxml.etree.HTML(pagedata)  # 编码
        '''   
        正则提取
        pagenum = mytree.xpath("//*[@class = 'td']/text()")      #['共111页，到第', '页']
        print(pagenum)
        print(pagenum[0])   #共111页，到第
        pag = re.compile(r"(\d+)",re.IGNORECASE)
        pagenumber =pag.findall(pagenum[0])
        pagenumber= eval(pagenumber[0])   #111 <class 'int'>
        print(pagenumber,type(pagenumber))
        '''
        worktext = mytree.xpath("//div[@class='el']/p/span/a/@href")  # 连接
        for a in worktext:
            # print(lxml.etree.tostring(a))
            urlset.add(a)
        # for i in urlset:
        #     print(i)
        # print(urlset)
        return urlset









'''
url = "http://search.51job.com/jobsearch/search_result.php?fromJs=1&jobarea=010000&keyword=python&keywordtype=2&lang=c&stype=2&postchannel=0000&fromType=1&confirmdate=9"
page = GetUrl(url,"utf-8")
page.get_51job()

'''




