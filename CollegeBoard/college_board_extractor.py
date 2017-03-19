


from bs4 import BeautifulSoup
from multiprocessing import Pool
from time import time
import csv
import os 
import re


fields = [  'University', 
            'City',       
            'State' ]
#            'Enrollment (Undergrad)', 
#            'Male Enrollment', 
#            'Female Enrollment',
#            'Native Hawaiian/Pacific Islander', 
#            'American Indian/Alaskan Native', 
#            'Multi-race (not Hispanic/Latino)', 
#            'Asian', 
#            'White', 'Black/African-American', 
#            'International', 
#            'Hispanic/Latino', 
#            'Unknown']

def scrape_html(html):
    row = dict.fromkeys(fields)


    try:
        with open(html) as f:
            soup = BeautifulSoup(f, 'lxml')
            title = soup.find("td", class_="col2 alignRight") 
            row['University'] = title.find('h1').text
            row['City'] = title.find('h2').text.split(',')[0]
            row['State'] = title.find('h2').text.split(',')[1]

    except:
        pass


    return row





if __name__ == '__main__':
    csv_dir = 'CSV'

    html_dir = 'HTML'

    cwd = os.path.join(os.getcwd(), html_dir)

    files = [os.path.join(cwd, file) for file in os.listdir(html_dir)]

    pool = Pool(processes=8)

    t0 = time()
    data = pool.map(scrape_html, files)

    with open("CollegeBoard.csv", "w", newline='') as f: 
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        for row in data:
            writer.writerow(row)

    print("Time Elapsed: %0.3f" % (time() - t0))

    #path = os.path.join("HTML", "000539.html")
    #with open(path, "r") as f: 
    #    scrape_html(f)
