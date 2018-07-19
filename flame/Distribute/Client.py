#coding:utf-8
import multiprocessing
import multiprocessing.managers
import queue

import flame.crawl_data.Crawl_Data
import flame.crawl_data.Merge_Url
import flame.crawl_page.GetDataFromFunc_xpath

class QueueManger(multiprocessing.managers.BaseManager):
    pass

if __name__ == '__main__':
    QueueManger.register("get_task")
    QueueManger.register("get_result")
    QueueManger.register("get_status")
    manage = QueueManger(address=("10.0.123.250",8848),authkey=b"111111")
    manage.connect()
    task,result,status = manage.get_task(),manage.get_result(),manage.get_status()
    url = task.get()
    try:
        urlset = flame.crawl_page.GetDataFromFunc_xpath.GetUrl(url,"utf-8")
    except:
        urlset = flame.crawl_page.GetDataFromFunc_xpath.GetUrl(url, "gbk")


    searchname=task.get()[1]
    searchtype=task.get()[2]
    flame.crawl_data.Crawl_Data.CrawlData(searchname,searchtype,result)
    status .put(1)