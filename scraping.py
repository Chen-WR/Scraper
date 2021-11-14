from selenium import webdriver
from selenium.webdriver.common.by import By
from PIL import Image
from bs4 import BeautifulSoup
import time
import os
import sys

target = sys.argv[1]


base_path = "C:\\Users\\CR\\Downloads"
temp_path = os.path.join(base_path,target)
resize_path = os.path.join(base_path,f"resize_{target}")
if not os.path.exists(temp_path):
	os.mkdir(temp_path)
if not os.path.exists(resize_path):
	os.mkdir(resize_path)

url = f"https://www.pexels.com/search/{target}/"
chrome_options = webdriver.ChromeOptions()
prefs = {'download.default_directory' : temp_path}
chrome_options.add_experimental_option('prefs', prefs)
chrome_options.add_argument("--start-maximized")
chrome_options.add_argument('--disable-gpu')
driver = webdriver.Chrome(options=chrome_options)
driver.get(url)



def infiniteScroll():
	total_time = 0
	total_scroll = 500
	scroll = 0
	while scroll < total_scroll:
		start = time.time()
		try:
			driver.execute_script(f'window.scrollTo(0,{driver.execute_script("return document.body.scrollHeight;") - 800})')
			time.sleep(1)
		except:
			break
		print(f'Scroll: {scroll}')
		print(f'>>>>>>>>>>>>>>>>>>Time used: {time.time()-start}')
		total_time += (time.time()-start)
		print(f'>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>Total Time: {total_time}')
		scroll+=1

def makeSoup():
	html = driver.page_source
	lists = []
	soup = BeautifulSoup(html,'lxml')
	elements = soup.find_all(class_="ButtonGroup_downloadButton__1m5vg",href=True)
	for element in elements:
		link = element['href']
		lists.append(link)
	return set(lists)

def makeSets():
	# sets = set()
	# while len(sets) < limit:
	sets = sets.union(set([link.get_attribute("href") for link in driver.find_elements(by=By.CLASS_NAME,value="ButtonGroup_downloadButton__1m5vg")]))
	return sets

def downloadImage(sets):
	total = len(sets)
	for pic in sets:
		driver.get(pic)
		total-=1
		print(f'{total} download left')
		time.sleep(0.2)

def processImage(path):
	total = len(os.listdir(path))
	for file in os.listdir(path):
		if not ".crdownload" in file:
			img_path = os.path.join(path,file)
			img = Image.open(img_path)
			old_location = img.filename
			new_location = os.path.join(resize_path,old_location[len(path)+1:])
			resized = img.resize(size=(220,220))
			# resized.save(new_location,optimize=True,quality=10)
			resized.save(new_location)
			os.remove(old_location)
			total -= 1
			print(f"{total} picture remaining to process")



def start():
	infiniteScroll()
	# sets = makeSets()
	sets = makeSoup()
	downloadImage(sets)
	processImage(temp_path)


start()