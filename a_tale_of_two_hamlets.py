import math
import os
from text_markov import TextMarkov


NGRAM_SIZE = 5
ITERATIONS = 10000


def load_text(filepath):
    print('loading file: %s...' % (filepath,))
    markov = TextMarkov(NGRAM_SIZE)
    book_file = open(filepath)
    for line in book_file.readlines():
        markov.read_text(line.strip('\n'))
    print('%s successfully loaded' % (filepath,))
    return markov


def get_weight(markov_model, *ngram):
    prefix = ngram[:-1]
    suffix = ngram[-1]
    if suffix not in markov_model.get_suffixes(*prefix):
        return 0.0
    else:
        return markov_model.get_suffixes(*prefix)[suffix]


if __name__ == '__main__':
    bible_markov = load_text('books/hamlet.txt')
    two_cities_markov = load_text('books/a_tale_of_two_cities.txt')

    print('merging markov models...')
    merge_markov = TextMarkov(NGRAM_SIZE)
    merge_markov.update(bible_markov)
    merge_markov.update(two_cities_markov)
    print('markov merge complete')

    print('generating random texts...')
    texts = []
    for i in range(ITERATIONS):
        text = merge_markov.random_text()
        ngram_diffs = []
        text_tokens = merge_markov.tokenize(text)
        total_bias = 0.0
        for i in range(len(text_tokens)-merge_markov.n):
            j = i + merge_markov.n
            ngram = text_tokens[i:j]
            ngram_diff = get_weight(bible_markov, *ngram) - get_weight(two_cities_markov, *ngram)
            ngram_diffs.append(ngram_diff)
            total_bias += ngram_diff
        text_diff = 0
        for i in range(len(ngram_diffs)-1):
            text_diff += abs(ngram_diffs[i+1]-ngram_diffs[i])
        mean_text_diff = text_diff / math.log(len(text_tokens))
        texts.append((text, mean_text_diff-abs(total_bias), ngram_diffs))
    print('random texts generation complete')
    
    print('ordering texts...')
    texts.sort(key=lambda x: x[1])
    print('top text:')
    top = texts[-1]
    text = top[0]
    diff_shift = top[1]
    diffs = ' '.join('%.2f' % (diff,) for diff in top[2])
    print('\n%.2f\n\n%s\n%s\n' % (diff_shift, text, diffs))
