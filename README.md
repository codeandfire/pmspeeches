This dataset contains the full text of 1000+ speeches given by the current Prime Minister of India, Narendra Modi, from August 2014 up to July 2021.

The full text of these speeches are publicly available at <https://www.pmindia.gov.in/en/tag/pmspeech/> and have been scraped using [Selenium](https://pypi.org/project/selenium/) and [Beautiful Soup](https://pypi.org/project/beautifulsoup4/).

This is a bilingual dataset in English and Hindi. The speeches are primarily given in one of the two languages, with slight intermixing in between.

### Requirements

This code has been run using Python 3.9 and the following package versions:
````
beautifulsoup4==4.9.3
langdetect==1.0.9
nltk==3.6.2
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
$ python get_links.py
````

This will create a `links.pkl` file in your current directory. For me, this took about 10 minutes to run.

Next, download the actual transcripts of the speeches using `extract_speeches.py`.

````
$ python extract_speeches.py
````

This can take an hour or so to run. You will see your current directory getting filled up with `.txt` files containing the speech transcripts.

This script also creates a log file `extract_speeches.log` in the current directory, containing the URLs of speeches that failed to download correctly. Typically, these are the results of timeouts: you should run `extract_speeches.py` again on these URLs, and they should download correctly this time. (You can do this by extracting the URLs mentioned in the log file into a list of strings, and saving it to `links.pkl` using Python's `pickle` library. Note that you only have to look at URLs in entries prefixed with

````
WARNING:root
````
in the log file, and not the other entries of the log file.)

Finally, move the `*.txt` files to a directory named `dataset` and run

````
$ python split_en_hi.py dataset
````

to split the speeches into English and Hindi speeches. You will first need to install

````
$ pip install langdetect
````
for this.

(A few files may not get placed into either directory. These are typically empty files: delete them.)


### Stats

To get some quick statistics on this corpus, run `stats.py`. First, you will need to install `nltk`:

````
$ pip install nltk
````

and then run in a Python interpreter

````python
>>> import nltk
>>> nltk.download('punkt')
>>> nltk.download('stopwords')
````

Finally, run

````
$ python stats.py dataset
````
where `dataset` is the directory containing the dump of `*.txt` transcript files. You should get the following output:

````
676 English speeches, 425 Hindi speeches.

Among English speeches ...
        65948 total sentences.
        546905 tokens with stopwords removed, 22974 unique.
        TTR = 0.042

Most frequent tokens with counts:
        india           8687
        country         5476
        people          4479
        friends         4150
        today           3890
        new             3412
        world           3367
        government      2747
        time            2222
        years           2166
        work            1985
        like            1735
        development     1730
        ji              1730
        indian          1420
        farmers         1381
        make            1371
        year            1316
        great           1298
        made            1292
        important       1283
        countries       1249
        come            1202
        last            1179
        take            1163
````
or something similar if you have scraped the dataset yourself.

(The statistics are primarily for the English speeches. That is because `nltk` does not support Hindi out-of-the-box, and while there are other libraries such as [indic-nlp-library](https://pypi.org/project/indic-nlp-library/) available, I haven't tried them out.)
