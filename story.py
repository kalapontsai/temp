import urllib.request
from bs4 import BeautifulSoup
import json
import random
import string

next_url = ''
sentences = []
book = 0

with open('bookmark.json', encoding='utf8') as f:
	json_data = json.load(f)
	tid = str(json_data[book]['url']['tid'])
	sid = str(json_data[book]['url']['sid'])
print('Current book is %s ' % str(json_data[book]['name']))

while 1:
	url = 'https://sj.uukanshu.com/read.aspx?tid=' + tid + '&sid=' + sid
	print(url)
	url_page = urllib.request.urlopen(url)
	soup = BeautifulSoup(url_page,'html.parser')
	pre_url = soup.find(id='read_pre')['href']
	next_url = soup.find(id='read_next')['href']

	for s in soup.findAll('div','ad_content'):
		s.extract()
	for s in soup.findAll('script'):
		s.extract() 

	name_box = soup.find('p')
	txt_content = name_box.get_text()

	sentences = str.split(txt_content,"。") 
	count = 0
	for i in sentences:
		count += 1
		print(i)
		print('------------------------------------------\r\n')
		gap_txt = ""
		for gap in range(1500):
			gap_txt += random.choices(string.printable)[0]
		print (gap_txt)
		input("\r\npress enter key (%i / %i).....\r\n" % (count,len(sentences)))

	cmd = input("Pre(1) / Next(0) :")
	if (cmd == "1"):
		sid = str(pre_url[pre_url.find('sid=')+4:])
	elif (cmd == "0"):
		sid = str(next_url[next_url.find('sid=')+4:])
	else:
		print("Unknow command ~~~~~~~~")
		break

	json_data[book]['url']['sid'] = sid
	with open('bookmark.json','w') as f:
		json.dump(json_data,f)
