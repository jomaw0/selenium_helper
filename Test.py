from selenium_helper.SeleniumHelper import *
from selenium_helper.PageControl import *
import time

class TestPageControl(PageControl):
	def other(self):
		print('other')
	
	def execute(self):
		print('moin')
	
	def scrapeDetail(self):
		print('detail')

helper = SeleniumHelper()
helper.start()
helper.open('https://google.de')

control = TestPageControl(helper)
control.scrapeDetail()
control.other()

time.sleep(5)