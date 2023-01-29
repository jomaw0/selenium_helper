from abc import ABC, abstractmethod

class PageControl(ABC):
	def __init__(self, helper):
		self.helper = helper
	
	@abstractmethod
	def execute(self):
		print('scrape multiple')
	
	@abstractmethod
	def scrapeDetail(self):
		print('detail')