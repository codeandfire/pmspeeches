import pickle
import time

from bs4 import BeautifulSoup
from selenium import webdriver

# replace Edge with your own browser here.
# ensure that you have installed the appropriate driver for your browser
# and point executable_path to the driver's executable.
driver = webdriver.Edge(executable_path='C:/tools/edgedriver_win64/msedgedriver.exe')

driver.get('https://www.pmindia.gov.in/en/tag/pmspeech/')

prev_height = None
while True:

    # scroll down the page.
    driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')

    # wait for further results to load.
    time.sleep(5)

    # if there are no further results, the height of the page remains the same.
    new_height = driver.execute_script('return document.body.scrollHeight')
    if new_height == prev_height:
        break
    prev_height = new_height

page_source = driver.page_source
driver.close()

soup = BeautifulSoup(page_source, 'html.parser')

# find all the URLs in the page.
links = [a_tag.get('href') for a_tag in soup.find_all('a')]

# some of the URLs are None.
# they need to be removed or they raise an error in the next step.
links = [l for l in links if l is not None]

# a simple analysis of the links shows that the URLs that point to speeches
# contain the terms news_updates and tag_term=pmspeech
links = [l for l in links if "news_updates" in l and "tag_term=pmspeech" in l]

# many of the links are duplicates, remove duplicates while maintaining order.
links = sorted(set(links), key=lambda x: links.index(x))

with open('links.pkl', 'wb') as f:
    pickle.dump(links, f)
