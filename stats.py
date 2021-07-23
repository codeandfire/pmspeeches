from collections import Counter
import os
import sys

from nltk.corpus import stopwords
from nltk.tokenize import sent_tokenize, word_tokenize

# number of most frequent tokens to display.
DISPLAY_TOKENS = 25

raw_text = ""
en_docs = 0
for entry in os.scandir(os.path.join(sys.argv[1], 'en')):
    with open(entry.path, 'r', encoding='utf-8', errors='ignore') as f:
        raw_text = raw_text + ' ' + f.read()
        en_docs += 1

hi_docs = len(os.listdir(os.path.join(sys.argv[1], 'hi')))

print(f"{en_docs} English speeches, {hi_docs} Hindi speeches.")
print()
print("Among English speeches ...")

raw_text = raw_text.lower()
sents = sent_tokenize(raw_text)
tokens_per_sent = [word_tokenize(s) for s in sents]
tokens = [t for token_list in tokens_per_sent for t in token_list]

stop_tokens = stopwords.words('english')

# some additional stopwords.
stop_tokens = stop_tokens + ['also', 'one', 'many', 'us', 'every', 'would']

tokens = [t for t in tokens if t not in stop_tokens and t.isalpha()]
vocab = Counter(tokens)

S, T, V = len(sents), len(tokens), len(vocab)
ttr = V/T
print(f"\t{S} total sentences.")
print(f"\t{T} tokens with stopwords removed, {V} unique.")
print(f"\tTTR = {ttr:.3f}")

disp_tokens = vocab.most_common(DISPLAY_TOKENS)
max_token_length = max([len(tok) for tok, cnt in disp_tokens])

max_count = disp_tokens[0][1]
d = 1
while True:
    if max_count < 10**d:
        max_count_digits = d
        break
    d = d + 1

print()
print("Most frequent tokens with counts:")
fmt = "\t{token:{max_token_length}}\t{count:{max_count_digits}}"
for token, count in disp_tokens:
    print(
        fmt.format(
            token=token,
            max_token_length=max_token_length,
            count=count,
            max_count_digits=max_count_digits
        )
    )
