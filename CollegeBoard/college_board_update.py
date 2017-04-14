from bs4 import BeautifulSoup
from multiprocessing import Pool
from time import time
import csv
import os 
import re
import validators


fields = [  'University',
            'services',
            'website'    ]


restricted = set(['PR', 'VI'])

def scrape_html(html):
    row = dict.fromkeys(fields)

    try:
        with open(html) as f:
            soup = BeautifulSoup(f, 'lxml')
            title = soup.find("td", class_="col2 alignRight") 
            row['University'] = title.find('h1').text
            state = title.find('h2').text.split(',')[1].strip()
            if len(state) != 2 or state in restricted:
                return  

            p = soup.find('h2', text=r"Counseling And Wellness")
            services = [s.text.strip() for s in p.parent.find_all('p')]
            row['services'] = '; '.join(services)

            for c in soup.find('h2', text=r"Main Address").parent.children:
                if 'www.' in str(c.string):
                    row['website'] = str(c.string)

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

    with open("CollegeBoardUpdate.csv", "w", newline='') as f: 
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        for row in data:
            if row != None:
                writer.writerow(row)

    print("Time Elapsed: %0.3f" % (time() - t0))

    #path = os.path.join("HTML", "000539.html")
    #with open(path, "r") as f: 
    #    scrape_html(f)
