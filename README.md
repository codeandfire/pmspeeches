This dataset contains the full text of 1000+ speeches given by the current Prime Minister of India, Narendra Modi, from August 2014 up to July 2021.

The full text of these speeches are publicly available at <https://www.pmindia.gov.in/en/tag/pmspeech/> and have been scraped using [Selenium](https://pypi.org/project/selenium/) and [Beautiful Soup](https://pypi.org/project/beautifulsoup4/).

This is a bilingual dataset in English and Hindi. The speeches are primarily given in one of the two languages, with slight intermixing in between.

### Requirements

This code has been run using Python 3.9 and the following package versions:
````
beautifulsoup4==4.9.3
langdetect==1.0.9
selenium==3.141.0
tqdm==4.61.2
urllib3==1.26.6
````

### Scraping

You can perform the scraping yourself using the two short scripts `get_links.py` and `extract_speeches.py`. First, install Selenium and BeautifulSoup:
````
$ pip install selenium beautifulsoup4
````
as well as
````
$ pip install tqdm urllib3
````
Then run `get_links.py`. This script has been written assuming you use Microsoft Edge as your browser. It can be easily changed for another browser: see the source code of this script for directions.
````
$ python scraping/get_links.py
````
This will create a `links.pkl` file in your current directory. For me, this took about 10 minutes to run.

Next, download the actual transcripts of the speeches using `extract_speeches.py`.
````
$ python scraping/extract_speeches.py
````
This can take an hour or so to run. You will see your current directory getting filled up with `.txt` files containing the speech transcripts.

This script also creates a log file `extract_speeches.log` in the current directory, containing the URLs of speeches that failed to download correctly. Typically, these are the results of timeouts: you should run `extract_speeches.py` again on these URLs, and they should download correctly this time. You can do this as follows: in Bash on Linux, you can run
````bash
$ grep "^WARNING:root" extract_speeches.log | grep -o "https.*" | sort | uniq > links.txt
````
to extract the URLs which have failed to download, and then in Python
````python
>>> with open('links.txt', 'r') as f:
	links = f.read().splitlines()
>>> import pickle
>>> with open('links.pkl', 'wb') as f:
	pickle.dump(links, f)
````
Then, run
````
$ python scraping/extract_speeches.py
````
Finally, delete `links.txt`:
````bash
$ rm links.txt
````

Now, move the `*.txt` files to a directory named `dataset`. On Linux, you can do this using
````bash
$ mkdir dataset
$ mv *.txt dataset/
````
Finally, run
````
$ python scraping/split_en_hi.py dataset
````
to split the speeches into English and Hindi speeches. You will first need to install
````
$ pip install langdetect
````
for this.

(A few files may not get placed into either of the `en` or `hi` directories. These are typically empty files: delete them.)


### Exploration

To get some basic insights from this dataset, take a look at the file `exploration.md`.
