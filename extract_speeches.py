import datetime
import logging
import pickle
from urllib3 import PoolManager
from urllib3.exceptions import MaxRetryError

from bs4 import BeautifulSoup
from tqdm import tqdm

# set up a log file
logging.basicConfig(filename='extract_speeches.log')

with open('links.pkl', 'rb') as f:
    links = pickle.load(f)

# timeout requests after 5 seconds.
http = PoolManager(timeout=5)

# tqdm displays a nice progress bar.
for url in tqdm(links, desc='downloading'):

    try:
        data = http.request('GET', url).data
    except MaxRetryError:
        logging.warning(f"Request to {url} timed out")

    soup = BeautifulSoup(data, 'html.parser')

    # a simple analysis of the HTML shows us that the transcript of the
    # speech is contained in a <div> tag of the form
    # <div class='news-bg'>
    #     <p>...</p>
    #     <p>...</p>
    #     ...
    #     <p>...</p>
    # </div>
    # so we use soup to search for that <div> tag and retrieve its contents,
    # which is essentially a sequence of <p> tags and \n characters.
    # note that we could always fall back to soup.get_text(), but this
    # may give us better results.
    try:
        contents = [
            p_tag.string
            for p_tag in soup.find('div', 'news-bg').contents
            if p_tag != '\n'
        ]

    except AttributeError:
        logging.warning(f"No <div> of class 'news-bg' found for speech with url {url}")
        continue

    # some of the <p> tags turn out to be empty at times.
    contents = ' '.join([c for c in contents if c is not None])

    # get <title> of the speech.
    try:
        title = soup.title.string
    except AttributeError:
        logging.warning(f"No <title> found for speech with url {url}")
        continue

    # the actual title of the speech is always followed by a redundant
    # suffix " | Prime Minister of India".
    # remove that suffix.
    title = title[:title.index('|')]

    # retain only alphanumeric characters and spaces.
    # then replace spaces with hyphens.
    title = ''.join([
        c for c in title.strip().lower() 
        if c.isalpha() or c.isdigit() or c == ' '
    ]).replace(' ', '-')

    # get date the speech was made.
    # a simple analysis of the HTML shows us that the date is contained in
    # a <span> tag with class='date'
    try:
        date = soup.find('span', 'date').string
    except AttributeError:
        logging.warning(f"No <span> of class 'date' found for speech with url {url}")
        continue

    # the date is in the format "<day> <monthname>, <year>"
    # for e.g. "19 Jul, 2021".
    # convert it to the standard YYYY-MM-DD format and prefix it to the title.
    date = datetime.datetime.strptime(date, '%d %b, %Y').strftime('%Y-%m-%d')
    title = date + '-' + title

    # encoding='utf-8' is required because of hindi text.
    with open(title+'.txt', 'w', encoding='utf-8', errors='ignore') as f:
        f.write(contents)
