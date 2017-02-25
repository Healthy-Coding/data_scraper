
from bs4 import BeautifulSoup
import csv
import os 
import re

html_dir = 'HTML'


for f in os.listdir(html_dir):
	# Skip the readme file
	if f == "README.md":
		continue

	path = os.path.join(html_dir, f)
	with open(path) as html: 
		soup = BeautifulSoup(html, 'lxml')

		# College Information
		title = soup.find("div", class_="cp_left")	
		uni_name = title.find("h1").get_text()
		uni_city, uni_state = title.find("p").get_text().strip().split(",")

		undergrad_data = soup.find('th', text="Undergraduate Students")

		uni_size = undergrad_data.next_sibling.text

		# Gender information
		women = undergrad_data.parent.next_sibling.next_sibling
		enrolled_women = women.find('td').text.split()[0]

		men = women.next_sibling.next_sibling
		enrolled_men = men.find('td').text.split()[0]

		# Economic information
		#money = soup.find('th', text="Cost of Attendance")
		#print("Cost: " + money.next_sibling.text)

		# Greek life data -- would need to be incorporated  
		#frat = soup.find('th', text="Fraternities")
		#print("Frat: " + frat.next_sibling.text)
		#soro = soup.find('th', text="Sororities")
		#print("Soro: " + soro.next_sibling.text)

		ethnicity = soup.find('th', text="Ethnicity of Students from U.S.")

		ethnicity_dict = {}

		for x in ethnicity.next_sibling.children:
			if x.string != None:
				try:
					perc, nationality = x.string.split("%")
					ethnicity_dict[nationality.strip()] = perc
				except ValueError: 
					print("ERROR")
					print(x.string)
		# International student data -- internat[2] is the number of countries
		internat = soup.find('th', text="International Students").next_sibling.text.split()
		p_internat = internat[0]

		ethnicity_dict["international"] = p_internat
		ethnicity_dict["uni name"] = uni_name

		if len(ethnicity_dict) != 10:
			print(uni_name + " " + str(len(ethnicity_dict)))

		# Write the dictionaries to two seperate csv files 
		#print(ethnicity_dict)

		#t = (uni_name, uni_state.strip(), uni_city, uni_size, enrolled_men, enrolled_women)

		#print(t)