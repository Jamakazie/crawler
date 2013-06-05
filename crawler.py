import urllib
import httplib
import os
import re
from bs4 import BeautifulSoup

class Crawler:
	baseurl = r'www.mangapanda.com'
	mangaurl = r'/93/naruto.html'
	title = 'naruto'
	mostRecent = 630
	def __init__(self):
		pass

	def __unicode__(self):
		return self.baseurl

	def __str__(self):
		return self.baseurl

	def getChapterUrls(self):
		chapters = {}
		conn =  httplib.HTTPConnection(self.baseurl)
		conn.request("GET", self.mangaurl) 
		resp = conn.getresponse()
		soup = BeautifulSoup(resp.read())
		for link in soup.find_all('a'):
			if str(link).find(self.title) != -1:
				chapterlink = link['href']
				chapternumber = re.sub('\D', '', link.get_text())
				if int(chapternumber) > self.mostRecent:
					print("Adding {0}".format(chapterlink))
					chapters[chapternumber] = chapterlink
		return chapters

	def getPageUrls(self):
		pages = []
		chapters = self.getChapterUrls()
		for key, value in chapters.items():
			page_urls = []
			conn = httplib.HTTPConnection(self.baseurl)
			conn.request("GET", value)
			resp = conn.getresponse()
			soup = BeautifulSoup(resp.read())
			pagez = soup.find('select', {'id' : 'pageMenu'})
			pagez = pagez.find_all('option')
			for page in pagez:
				page_urls.append(page['value'])
			pages.append(page_urls)
		return pages

	def getImageUrls(self, page_urls):
		image_urls = []
		for pages in page_urls:
			conn = httplib.HTTPConnection(self.baseurl)
			conn.request("GET", pages)
			resp = conn.getresponse()
			soup = BeautifulSoup(resp.read())
			title = soup.title.get_text()
			alt = re.sub('-[^-]+-', '-', title)
			url = soup.find('img', {'alt' : alt})
			image_urls.append(url['src'])
			#print soup.prettify() 
		dir_title = re.sub('-.*', '', alt).strip()
		print dir_title
		count = 1
		if not os.path.exists(dir_title):
			os.makedirs(dir_title)
		for images in image_urls:
			r = urllib.urlopen(images)
			image_file = r.read()
			image = open(dir_title+ '/' + str(count) + '.jpg', 'w')
			image.write(image_file)
			image.close()
			count += 1
	def crawl(self):
		pages = self.getPageUrls()
		for page in pages:
			self.getImageUrls(page)



x = Crawler()
x.crawl()
