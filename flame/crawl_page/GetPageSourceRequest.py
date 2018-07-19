# coding:utf-8

import urllib
import urllib.request
import selenium
import selenium.webdriver
import flame.crawl_page.GetPageSource
import requests
import chardet


class GetPageScourceRequest(flame.crawl_page.GetPageSource.GetPageSource):
    def __init__(self, url, decodetype):
        super(GetPageScourceRequest, self).__init__(url, decodetype)

    def getpagesource(self):
        chr = ""
        try:
            chr = requests.get(self.url, verify=True)  # 访问https
            chr.encoding = chardet.detect(chr.content)['encoding']
            # print(req.text)
            chr = chr.text
        except:
            try:
                chro = selenium.webdriver.Chrome()
            except:
                chro = selenium.webdriver.Firefox()
            chro.get(self.url)
            chr = chro.page_source
            chro.close()
        # print("获取网页源码成功")
        return chr


'''
test = GetPageScourceRequest("http://search.51job.com/list/010000,000000,0000,00,9,99,python,2,1.html?lang=c&stype=&postchannel=0000&workyear=99&cotype=99&degreefrom=99&jobterm=99&companysize=99&providesalary=99&lonlat=0%2C0&radius=-1&ord_field=0&confirmdate=9&fromType=&dibiaoid=0&address=&line=&specialarea=00&from=&welfare=","utf-8")
print (test.getpagesource())
'''
