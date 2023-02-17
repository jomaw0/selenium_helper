from selenium import webdriver 
from selenium.webdriver.chrome.options import Options 
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import pickle

class SeleniumHelper():
	def __init__(self, headless=False, remoteURL='', arguments=[]):
		self.startedBrowser = False
		self.headless = headless
		self.remoteURL = remoteURL
		self.arguments = arguments
		self.driver = None
		
	def _start_browser(self):
		chrome_options = Options()
		if self.headless:
			chrome_options.add_argument("--headless")
			
		for argument in self.arguments:
			chrome_options.add_argument(argument)
		chrome_options.add_argument('--disable-blink-features=AutomationControlled')
		chrome_options.add_argument("window-size=1280,800")
		chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36")
		
		if self.remoteURL == '':
			# use chrome driver manager
			self.driver = webdriver.Chrome(ChromeDriverManager().install(), options=chrome_options)
		else:
			# use remote driver
			self.driver = webdriver.Remote(command_executor=self.remoteURL, options=chrome_options)
		self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
		self.startedBrowser = True
		return self.driver
	
	## Start / Stop / Open
	# start
	def start(self):
		if self.startedBrowser:
			return False
		return self._start_browser()
		
	# quit
	def quit(self):
		if not self.startedBrowser:
			return
		self.startedBrowser = False
		self.driver.quit()
	
	def open(self, url):
		if not self.startedBrowser:
			self.start()
		self.driver.get(url)
		
		if self.page_has_loaded():
			return self.get_html()
		else:
			return False
	
	## Save Cookies
	def save_cookies(self, filepath):
		pickle.dump(self.driver.get_cookies(), open(filepath, 'wb'))
	
	def load_cookies(self, filepath):
		cookies = pickle.load(open(filepath, 'rb'))
		for cookie in cookies:
			self.driver.add_cookie(cookie)
	
	def clear_cookies(self):
		self.driver.delete_all_cookies()
	
	## Get URL / HTML
	# get html
	def get_html(self):
		if not self.startedBrowser:
			return False
		return self.driver.page_source
		
	def page_has_loaded(self):
		page_state = self.driver.execute_script('return document.readyState;')
		return page_state == 'complete'
	
	# URL
	def get_url(self):
		return self.driver.current_url
		
	## Input
	def click(self, element):
		element.click()
	
	def type(self, element, text):
		element.send_keys(text)
		
	## FIND
	# Private
	def _find_helper(self, timeout=20, itemType=EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'div'))):
		try:
			elements = WebDriverWait(self.driver, timeout).until(itemType)
			return elements
		except:
			return False
	
	def _find_children_from_element(self, element, css_selector):
		return element.find_elements(By.CSS_SELECTOR, css_selector)
		
	# Find
	def find_clickable_element(self, css_selector, timeout=20):
		itemType = EC.element_to_be_clickable((By.CSS_SELECTOR, css_selector))
		return self._find_helper(timeout=timeout, itemType=itemType)
	
	def find_element(self, css_selector, timeout=20):
		itemType = EC.presence_of_element_located((By.CSS_SELECTOR, css_selector))
		return self._find_helper(timeout=timeout, itemType=itemType)
	
	def find_elements(self, css_selector, timeout=20):
		itemType = EC.presence_of_all_elements_located((By.CSS_SELECTOR, css_selector))
		return self._find_helper(timeout=timeout, itemType=itemType)
		
	def find_map_by_attribute(self, css_selector, attribute):
		children = self.find_elements(css_selector)
		values = self.map_elements_by_attribute(children, attribute)
		return values
		
	# Children
	def find_child_from_element(self, element, css_selector):
		results = self._find_children_from_element(element, css_selector)
		value = results[0] if len(results) >= 1 else False
		return value
	
	def find_children_from_element(self, element, css_selector):
		return self._find_children_from_element(element, css_selector)
	
	# Attribute
	def get_attribute_from_element(self, element, attribute):
		return element.get_attribute(attribute)
	
	# Map
	def map_elements_by_attribute(self, elements, attribute):
		returnList = []
		for element in elements:
			value = self.get_attribute_from_element(element, attribute)
			returnList.append(value)
		return returnList
		
	def map_children_of_element_by_attribute(self, element, css_selector, attribute):
		children = self._find_children_from_element(element, css_selector)
		values = self.map_elements_by_attribute(children, attribute)
		return values