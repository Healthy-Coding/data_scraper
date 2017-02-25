
from bs4 import BeautifulSoup
import csv
import os 
import re

html_dir = 'HTML'

print("######################################################################")

for f in os.listdir(html_dir):
	path = os.path.join(html_dir, f)
	with open(path) as html: 
		soup = BeautifulSoup(html, 'lxml')
		title = re.sub(" Overview - CollegeData College Profile", "", soup.find('title').get_text())

		#for line in soup.find_all("tbody"):
		#	print(line)

		print("     " + title)
		print("----------------------------")

		undergrad = soup.find('th', text="Undergraduate Students")
		print("Total Enrollment (undergraduate): " +  undergrad.next_sibling.text)

		women = undergrad.parent.next_sibling.next_sibling
		print("Women: " + women.find('td').text)

		men = women.next_sibling.next_sibling
		print("Men: " + men.find('td').text)



		money = soup.find('th', text="Cost of Attendance")
		print("Cost: " + money.next_sibling.text)


		frat = soup.find('th', text="Fraternities")
		print("Frat: " + frat.next_sibling.text)
		soro = soup.find('th', text="Sororities")
		print("Soro: " + soro.next_sibling.text)

		print("---------------------------------------")
		ethnicity = soup.find('th', text="Ethnicity of Students from U.S.")

		for x in ethnicity.next_sibling.children:
			if x.string != None:
				print(x.string)


		internat = soup.find('th', text="International Students")

		print("International Students: " + internat.next_sibling.text)


		print("######################################################################")