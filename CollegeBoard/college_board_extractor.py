


from bs4 import BeautifulSoup
from multiprocessing import Pool
from time import time
import csv
import os 
import re


fields = [  'School ID', 
            'University', 
            'State', 
            'City', 
            'Enrollment (Undergrad)', 
            'Male Enrollment', 
            'Female Enrollment',
            'Native Hawaiian/Pacific Islander', 
            'American Indian/Alaskan Native', 
            'Multi-race (not Hispanic/Latino)', 
            'Asian', 
            'White', 'Black/African-American', 
            'International', 
            'Hispanic/Latino', 
            'Unknown']

def scrape_html(html):
    row = dict.fromkeys(fields)

    row['School ID'] = re.sub(".html", "",os.path.basename(html))

    try:
        with open(html) as f: 
            soup = BeautifulSoup(f, 'lxml')

            title = soup.find("div", class_="cp_left")  
            uni_name = title.find("h1").get_text()
            uni_city, uni_state = title.find("p").get_text().strip().split(",")

            row['University'] = uni_name
            row['State'] = uni_state.strip()
            row['City'] = uni_city

            undergrad_data = soup.find('th', text="Undergraduate Students")

            uni_size = undergrad_data.next_sibling.text

            if uni_size != 'Not reported':
                row['Enrollment (Undergrad)'] = int(re.sub(",", "", uni_size))

            # Gender information
            try:
                women = undergrad_data.parent.next_sibling.next_sibling
                enrolled_women = women.find('td').text.split()[0]

                men = women.next_sibling.next_sibling
                enrolled_men = men.find('td').text.split()[0]

                if enrolled_women != 'Not':
                    row['Male Enrollment'] = int(re.sub(",", "", enrolled_men))
                if enrolled_men != 'Not':
                    row['Female Enrollment'] = int(re.sub(",", "", enrolled_women))
            except Exception as e:
                pass

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
                        if nationality.strip() == 'Native Hawaiian/ Pacific Islander':
                            row['Native Hawaiian/Pacific Islander'] = perc
                        else:    
                            row[nationality.strip()] = perc
                    except ValueError: 
                        continue
            try:
                internat = soup.find('th', text="International Students").next_sibling.text.split()
                p_internat = internat[0]

                if p_internat != 'Not':
                    row["International"] = re.sub("%", "", p_internat)
            except Exception as e:
                pass

    except Exception as e:
        print(html)








if __name__ == '__main__':
	path = os.path.join("HTML", "000539.html")
	with open(path, "r") as f: 
		scrape_html(f)
