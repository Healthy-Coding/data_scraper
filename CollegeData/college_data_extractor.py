
from bs4 import BeautifulSoup
import csv
import os 
import re

def write_to_csv(csv_file, html_dir, state):
	with open(csv_file, 'w', newline='') as data: 
		fieldnames = ['University', 'State', 'City', 'Enrollment (Undergrad)',
						'Male Enrollment', 'Female Enrollment',
						'Native Hawaiian/ Pacific Islander', 
						'American Indian/Alaskan Native', 
						'Multi-race (not Hispanic/Latino)', 'Asian', 
						'White', 'Black/African-American', 'International', 
						'Hispanic/Latino', 'Unknown']

		writer = csv.DictWriter(data, fieldnames=fieldnames)
		writer.writeheader()

		for f in os.listdir(os.path.join(html_dir, state)):
			row = dict()

			with open(os.path.join(html_dir, state, f)) as html: 
				soup = BeautifulSoup(html, 'lxml')


				title = soup.find("div", class_="cp_left")	
				uni_name = title.find("h1").get_text()
				uni_city, uni_state = title.find("p").get_text().strip().split(",")

				row['University'] = uni_name
				row['State'] = uni_state.strip()
				row['City'] = uni_city
 
				undergrad_data = soup.find('th', text="Undergraduate Students")

				uni_size = undergrad_data.next_sibling.text

				if uni_size == 'Not reported':
					continue

				row['Enrollment (Undergrad)'] = int(re.sub(",", "", uni_size))

				# Gender information
				women = undergrad_data.parent.next_sibling.next_sibling
				enrolled_women = women.find('td').text.split()[0]

				men = women.next_sibling.next_sibling
				enrolled_men = men.find('td').text.split()[0]

				if enrolled_women == 'Not':
					continue
				if enrolled_men == 'Not':
					continue

				row['Male Enrollment'] = int(re.sub(",", "", enrolled_men))
				row['Female Enrollment'] = int(re.sub(",", "", enrolled_women))


				# Economic information
				#money = soup.find('th', text="Cost of Attendance")
				#print("Cost: " + money.next_sibling.text)

				# Greek life data -- would need to be incorporated  
				#frat = soup.find('th', text="Fraternities")
				#print("Frat: " + frat.next_sibling.text)
				#soro = soup.find('th', text="Sororities")
				#print("Soro: " + soro.next_sibling.text)

				ethnicity = soup.find('th', text="Ethnicity of Students from U.S.")

				for x in ethnicity.next_sibling.children:
					if x.string != None:
						try:
							perc, nationality = x.string.split("%")
							row[nationality.strip()] = perc
						except ValueError: 
							continue

				internat = soup.find('th', text="International Students").next_sibling.text.split()
				p_internat = internat[0]

				if p_internat == 'Not':
					continue

				row["International"] = re.sub("%", "", p_internat)

				for field in fieldnames: 
					if field not in row:
						continue
						#row[field] = None

				writer.writerow(row)

if __name__ == '__main__':
	csv_file = 'ga_college_data.csv'
	csv_dir = 'CSV'

	html_dir = 'HTML'
	state = 'GA'

	write_to_csv(os.path.join(csv_dir, csv_file), html_dir, state)
