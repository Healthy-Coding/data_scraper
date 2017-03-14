
import urllib.request

from time import time, gmtime, strftime
import sys
import os

base_url = "https://bigfuture.collegeboard.org/college-university-search/print-college-profile?id="

# String to look for defining a non-existant page
not_found = "Sorry, we can't find the page you're looking for."

save_dir = "HTML"

# When to exit the loop
MAX_INVALID = 20


def crawl():
    school_id = 113

    invalid_links = 0

    t0 = time()
    while invalid_links < MAX_INVALID:
        sys.stdout.write("\rSchool ID: %i" % school_id)
        sys.stdout.flush()

        try:
            url = base_url + str(school_id)
            html = urllib.request.urlopen(url).read()

            path = os.path.join(save_dir, "%06d.html" % school_id)
            with open(path, 'wb') as f:
                f.write(html)

            invalid_links = 0

        except urllib.error.HTTPError:
            invalid_links += 1

        school_id += 1


    sys.stdout.write("\n")

    print("Time Elapsed: %0.3f" % (time() - t0))
    print("Date: " + strftime("%a, %d %b %Y %H:%M:%S", gmtime()))


if __name__ == '__main__':
    crawl()
