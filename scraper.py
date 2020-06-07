import requests
import time
from tqdm import tqdm
from bs4 import BeautifulSoup
import pandas as pd
import os

jobs = []  # List to store job title
items = []  # list to store html tags that contain job title


def get_Items(url):
    """Get all jobs inside a specific html tag by requesting a page and then search for div tags."""
    request = requests.get(url)
    soup = BeautifulSoup(request.text, 'html.parser')
    # extract all div tags that we can (depend on the html page you want to scrape)
    return soup.findAll('div', attrs={'class': 'JobSearchCard-primary-heading'})


print('*- enter the number of the pages that you want to scrap:')
x = input()
print("start counting  job  per page...")
with tqdm(total=int(x)) as pbar:
    for i in range(0, int(x)):
        url = 'https://www.freelancer.com/work/projects/'+str(i)+'/'
        items = items+get_Items(url)
        pbar.update(1)   # update progress bar by one
print('there is '+str(len(items))+' jobs')
print('would you like to initiate scraping  y/n')

if input() == 'y':

    with tqdm(total=len(items)) as pbar:
        for a in items:
            # get child elemnt of the div tag (see function at beginning)
            name = a.find( 'a', attrs={'class': 'JobSearchCard-primary-heading-link'})
            jobs.append(name.text.strip())
            time.sleep(.01)
            pbar.update(1)   # update progress bar by one
    print("scraping completed !")

    df = pd.DataFrame({'Jobs': jobs})
    df.to_csv('d://jobs.csv', encoding='utf-8', index=False, header=True)  # save scraped data to csv file
    os.startfile('d://jobs.csv')  # launch the file
else:
    pass
