"""
	Author: Xavid Ramirez
	Desc: Bot to crawl onto linkedin and send out invitations to
		  users based on search criteria. To be used for educational
		  purposes when developing crawlers dealing with hidden elements.
"""
import time
from selenium import webdriver
from selenium.webdriver.common.by import By 
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC 
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains

#GLOBAL VALUES USED IN SCRIPT
url = "https://www.linkedin.com/uas/login?goback=&trk=hb_signin"
url_2 = 'https://www.linkedin.com/search/results/people/?facetNetwork=%5B%22S%22%5D&keywords=microsoft&origin=FACETED_SEARCH'
base_search_URL = 'https://www.linkedin.com/search/results/people/?facetNetwork=%5B"S"%5D&keywords='
#Webdriver Paths
Chromedriver_Path = r'PATH TO CROME DRIVER'
Chrome_Options = Options().add_argument('--test-type')
#END OF GLOBAL VALUES

# SCRAPPER CLASS AND IT'S METHODS
class LinkedInScrapper():

	def __init__(self,USERNAME,PASSWORD,MESSAGE,SEARCH):
		self.driver = webdriver.Chrome(Chromedriver_Path,chrome_options=Chrome_Options)
		self.username = USERNAME
		self.password = PASSWORD
		self.message = MESSAGE
		self.search = SEARCH
		self.driver.wait = WebDriverWait(self.driver,5)
	
	def Login(self):
		#lets get to the site
		self.driver.get(url)
		time.sleep(2)
		try:
			self.driver.find_element_by_name("session_key").send_keys(self.username)
			self.driver.find_element_by_name("session_password").send_keys(self.password+Keys.RETURN)
			time.sleep(2)	#give some time for the login.
		except Exception as a:
			print(str(a))

	def Search(self):
		#Lets search based on what keywords we chose
		#lets first compose the URL
		search_url = base_search_URL
		keywords = self.search.split(' ')
		last = keywords.pop(len(keywords)-1)	#last word
		for word in keywords:
			search_url += word + '%20'
		search_url += last + "&origin=GLOBAL_SEARCH_HEADER"	#add the last word and the end parameters
		self.driver.get(search_url)

	def nextPage(self):
		#Head to the next page
		time.sleep(2)	#lets wait for page to load
		Button = self.driver.execute_script("return document.querySelectorAll('button.next')[0]")
		if(Button != None):
			self.driver.execute_script("document.querySelectorAll('button.next')[0].click()")

	def send_notes(self):
		#This function queries all the buttons on the page
		#adding notes/invitations to only users who have not connected with you

		#Lets wait for the buttons to load
		WebDriverWait(self.driver,120).until(EC.presence_of_element_located((By.CSS_SELECTOR,".search-result__actions--primary.button-secondary-medium.m5")))
		#Lets grab all the buttons
		Buttons = self.driver.execute_script("return document.querySelectorAll('.search-result__actions--primary.button-secondary-medium.m5').length")
		for i in range(0,Buttons):
			#Check if button still says connect
			if("Connect" in self.driver.execute_script("return document.querySelectorAll('.search-result__actions--primary.button-secondary-medium.m5')["+str(i)+"].textContent")):
				self.driver.execute_script("document.querySelectorAll('.search-result__actions--primary.button-secondary-medium.m5')["+str(i)+"].click()")
				#Find the dialoug box that the Javascript brought up
				self.driver.execute_script("document.querySelectorAll('button.button-secondary-large')[1].click()")
				self.driver.find_element_by_name("message").send_keys(self.message)
				#send invitation
				self.driver.find_element_by_css_selector(".button-primary-large.ml3").click()
			#Done, lets wait for page to load a bit
			time.sleep(2)


## HERE WE WILL START THE SCRAPPER
def main(username,password,message,search_keywords):
	L = LinkedInScrapper(username,password,message,search_keywords)
	L.Login()
	L.Search()
	while True:
		L.send_notes()
		L.nextPage()

if __name__ == "__main__":
	#Call the function

	user_name = 'YOUR EMAIL'
	user_password = 'YOUR PASSWORD'
	user_message = 'WHAT MESSAGE YOU WANT TO SEND'
	user_search_keywords = 'SEARCH KEYWORDS HERE SEPARATED BY A SPACE'
	main(user_name,user_password,user_message,user_search_keywords)