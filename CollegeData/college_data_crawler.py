

from bs4 import BeautifulSoup

import urllib
import os
import re

import urllib.request

html_dir = "HTML"

k = 0
with open("college_data_ga_page3.html") as html:
	soup = BeautifulSoup(html, "lxml")

	for i in soup.find_all("li", class_="schoolInfo"):
		for a in i.find_all("a", href=True):
			# Seperate method?
			file = a.get_text().lower().strip()
			file = re.sub("[^a-z]", " ", file).split()
			file = "_".join(file) + ".html"
			url = a["href"]
			urllib.request.urlretrieve(url, os.path.join(html_dir, file))
			break
