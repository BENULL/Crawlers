import requests
from pyquery import PyQuery as pq
import pandas as pd
import time
import threading

class DocCrawler(threading.Thread,):

	def __init__(self):
		super(DocCrawler, self).__init__()
		self.headers = {
			'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36',
			'Connection': 'keep-alive',
			'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
			'Cookie': 'JSESSIONID=E39AB61FB602572D58399C1A0723EA83',
			'Accept': 'application/json, text/javascript, */*; q=0.01',
		}
		self.sess = requests.session()



	def run(self):
		print("%s is running" % threading.current_thread())
		while True:
			# 上锁
			gLock.acquire()
			global index_count
			if index_count == total_index:
				# 释放锁
				gLock.release()
				exit()
			else:
				index = index_count
				index_count += 1
				gLock.release()
				self.crawl(index)
				# if index % 10000 == 0 or index == total_index:
				# 	gLock.acquire()
				# 	print("保存一次", index)
				# 	info.to_excel('/Users/benull/Documents/PythonProject/Crawler/内容-江西3.xlsx')
				# 	gLock.release()
				# if index_count == total_index:
				# 	end = time.time()
				# 	print("消耗的时间为：", (end - start))
				# 	exit()

	def add_data(self,index, content):
		gLock.acquire()
		global info
		info.at[index, '内容'] = content
		gLock.release()

	def handle_resp(self,resp, query_url, index):
		try:
			resp.encoding = 'UTF-8'
			doc = pq(resp.text, parser='html')
			content = doc('div.article-info').text()
			self.add_data(index, content)
		except Exception as e:
			print(f'--第{index}个html解析错误')

	def crawl(self,index):
		query_url = data_link[index]
		print('--爬取第', index, '个')
		try:
			resp = self.sess.get(query_url, timeout=(2, 150), headers=self.headers)
			self.handle_resp(resp, query_url, index)
		except Exception as e:
			print(e)
			time.sleep(60)
			try:
				resp = self.sess.get(query_url, timeout=(2, 150), headers=self.headers)
				self.handle_resp(resp, query_url, index)
			except Exception as e:
				print(e)
				time.sleep(60)
				resp = self.sess.get(query_url, timeout=(2, 150), headers=self.headers)
				self.handle_resp(resp, query_url, index)


if __name__ == '__main__':
	info = pd.read_excel('/Users/benull/Documents/PythonProject/Crawler/标题重编-江西.xlsx')
	data_link = info['链接']
	total_index = 4001
	# total_index = len(info)-1
	index_count = 0
	gLock = threading.Lock()
	start = time.time()
	thread_list = []
	# 启动10个线程
	for x in range(10):
		t = Crawler()
		t.start()
		thread_list.append(t)
	for t in thread_list:
		t.join()
	info.to_excel('/Users/benull/Documents/PythonProject/Crawler/内容-江西4.xlsx')
	end = time.time()
	print("消耗的时间为：", (end - start))