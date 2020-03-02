MarkovMerge
=============

Contributors
------------

MarkovMerge is Connor Boyle's re-adaptation of his individual work for
TwitterBot. TwitterBot was a project for the course COMP 221 at Macalester
College, developed with teammates Ayoub Belemlih and Andrew Cui.

MarkovMerge consists entirely of Connor's original Python code, other than data
sources including tweets scraped by Ayoub circa 2016, as well as several books
downloaded and reformatted from Project Gutenberg.

About
-----

MarkovMerge is an experiment in combining distinct sets of textual training
data to create maximally "erratic" or "neutral" probabilistically generated
texts.

### What is a Markov Model?

A Markov model is a system for predicting the next element in a sequence based
solely on the previous few entries in the sequence. This can be used to
generate text, although there is generally no guarantee that the generated text
will at all resemble the training data, other than when viewed a few words at a
time.

### How Does MarkovMerge Model Text?

MarkovMerge processes textual data by first splitting it along word boundaries.
Unlike some other text-prediction Markov models, MarkovMerge treats the
punctuation and whitespace in between words as data of equal importance to the
words themselves. E.g. the following text:

```python
"Hello, how are you?"
```

will be split into the following tokens:

```python
"Hello" + ", " + "how" + " " + "are" + " " + "you" + "?"
```

if the user has chosen an n-gram size of 4, then occurrences of tokens will be
counted 4 tokens at a time:

```python
"Hello" + ", " + "how"  -> " "
", " + "how" + " "      -> "are"
```

etc., continued until the end of the text. Each recorded occurrence of a given
n-gram recorded in the source text increases the probability of generating the
last (in this case, 4th) element, after an occurrence the first `n - 1` (in
this case, 3) elements.

The script `single_demo.py` can demonstrate the text-demonstration capabilities
of the n-gram Markov model when used on one of the text sources included with
this project.


### How Does MarkovMerge Create Erratic Texts?

MarkovMerge can be trained on two distinct sources of texts. Separate models
will be stored for each source, as well as a third, combined model. The
combined model can then be used to probabilistically generate several (usually
on the order of several thousand) texts.

MarkovMerge can then go through each n-gram of each generated text and assign
the n-gram a "bias" value between -1.0 and 1.0, representing its relative
likelihood of being found in one source or another.  If a given n-gram is found
in source one but not source two, then the n-gram's bias is considered to be
`1.0`. If the n-gram is found in source two but not source one, then it has a
bias of `-1.0`.  If it is found in both sources, then the n-gram has a bias
equal to the probability of the n-gram being found in source one (i.e. share of
occurrences of the $n$th token after the first $n-1$ tokens) minus the
probability of the n-gram in source two.

MarkovMerge will then calculate the overall "movement" of each generated text
by summing the absolute difference in bias from one n-gram to the next.
MarkovMerge also calculates other metrics such as the "net bias" for a text,
which is defined as the sum of all biases of all n-grams in the text. A
generated text's "erraticity" is defined heuristically as its movement minus
the value of its net bias. I.e.:

```python
erraticity = movement - abs(net_bias)
```

Out of the thousands of generated texts, the one with the highest erraticity
score is selected and presented to the user. Each n-gram's suffix (its $n$th
element) is color-coded red, blue, or white, depending on its bias.


The script `merge_demo.py` is a proof of concept for this functionality.
