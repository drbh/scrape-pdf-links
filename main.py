from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import json

driver = webdriver.Firefox()
driver.get("https://www.google.com")

base_term = ""
site = "harvard.edu"

def input_and_enter(site):
	search_bar = driver.find_element_by_xpath("//input[@maxlength=\"2048\"]")
	search_expr = "site:{} kind:pdf " + base_term
	search_bar.send_keys(search_expr.format(site))
	time.sleep(1)
	search_bar.send_keys(Keys.RETURN)
	return 1

def get_links():
	return [ x.get_attribute("href") for x in driver.find_elements_by_tag_name("a")]

def get_pdf_links(x):
	if x is not None:
		return x[-4:] == ".pdf"
	return False


time.sleep(3)

did_search = input_and_enter(site)
pdf_links = []

try:
	for i in range(0, 20):
		time.sleep(1)
		links = get_links()
		pdf_links += list(filter(get_pdf_links, links))
		time.sleep(1)
		# go to next page
		driver.find_element_by_id("pnnext").click()

except Exception as e:
	pass

print("Found and saving",len(pdf_links))

with open('pdf_links.json', 'w') as json_file:
    json.dump(pdf_links, json_file, indent=4, sort_keys=True)