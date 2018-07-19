# coding:utf-8
import queue, time
import multiprocessing.managers
import multiprocessing
import threading


class QueueManger(multiprocessing.managers.BaseManager):
    pass


class StartDistribute(threading.Thread):
    task_queue = queue.Queue()
    status_queue = queue.Queue()

    def __init__(self, searchname, searchtype, resultqueue):
        super(StartDistribute, self).__init__()
        self.searchname = searchname
        self.searchtype = searchtype
        self.resultqueue = resultqueue

    def return_task(self):
        return self.task_queue

    def return_result(self):
        return self.resultqueue

    def return_status(self):
        return self.status_queue

    def run(self):
        multiprocessing.freeze_support()
        QueueManger.register("get_task", callable=self.return_task)
        QueueManger.register("get_result", callable=self.return_result)
        QueueManger.register("get_status", callable=self.return_status)
        manger = QueueManger(address=("10.0.123.250", 8848), authkey=b"111111")
        manger.start()
        task, status, result = manger.get_task(), manger.get_status(), manger.get_result()  # task,任务，resulit结果
        url = ''
        if self.searchtype == '51job':
            url = "http://search.51job.com/jobsearch/search_result.php?fromJs=1&jobarea=010000&keyword=" + self.searchname + "&keywordtype=2&lang=c&stype=2&postchannel=0000&fromType=1&confirmdate=9"
        elif self.searchtype == 'zhilian':
            pass
        elif self.searchtype == '51cto':
            pass
        else:
            pass

        task.put([url, self.searchname, self.searchtype])
        # 压入结果
        print("开始等待结果")
        count = 0
        for i in range(1000000):
            myresult = status.get(timeout=250)
            count += myresult
            if count == 10:
                break
        manger.shutdown()  # 关闭服务器


queue1 = queue.Queue()
a = StartDistribute('python', '51job', queue1)
a.start()
