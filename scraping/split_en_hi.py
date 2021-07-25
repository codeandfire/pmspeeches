import os
import shutil
import sys

from langdetect import detect
from langdetect.lang_detect_exception import LangDetectException

os.mkdir(os.path.join(sys.argv[1], 'en'))
os.mkdir(os.path.join(sys.argv[1], 'hi'))

for entry in os.scandir(sys.argv[1]):
    if entry.is_file():
        with open(entry.path, 'r', encoding='utf-8', errors='ignore') as f:
            try:
                lang = detect(f.read())
            except LangDetectException:
                # this is typically because the file is empty
                continue
        if lang == 'en':
            shutil.move(entry.path, os.path.join(sys.argv[1], 'en'))
        elif lang == 'hi':
            shutil.move(entry.path, os.path.join(sys.argv[1], 'hi'))
        else:
            print(f'{entry.name} detected as {lang}!')
