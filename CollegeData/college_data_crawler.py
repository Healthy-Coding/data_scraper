#
# This script opens a given url, checks if a string indicated a non-existant
# page is present, and saves the html to the disk if not.
# The main loop cuts out when there are X number of non-existant pages in a
# row (indicating it is most likely at the "end" of the website).
#
# Displays the current school_id on the screen and the elapsed time after.
#

import urllib.request

from time import time, gmtime, strftime
import sys
import os


base_url = "http://www.collegedata.com/cs/data/college/college_pg01_tmpl.jhtml?schoolId="

# String to look for defining a non-existant page
not_found = "You requested a College Profile page that does not exist. Please search again."

save_dir = "HTML"

# When to exit the loop
MAX_INVALID = 20

# Which school to start looking at
school_id = 1


def run():
    invalid_links = 0

    t0 = time()
    while invalid_links < MAX_INVALID:
        sys.stdout.write("\rSchool ID: %i" % school_id)
        sys.stdout.flush()

        url = base_url + str(school_id)
        html = urllib.request.urlopen(url).read()

        if not_found.encode() in html:
            invalid_links += 1
        else:
            path = os.path.join(save_dir, "%06d.html" % school_id)
            with open(path, 'wb') as f:
                f.write(html)
            invalid_links = 0

        school_id += 1

    sys.stdout.write("\n")

    print("Time Elapsed: %0.3f" % (time() - t0))
    print("Date: " + strftime("%a, %d %b %Y %H:%M:%S", gmtime()))


if __name__ == '__main__':
    run()
