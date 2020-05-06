MarkovMerge
=============

[Web Markov](https://github.com/cascadianblue/web-markov) is a web application
that allow users to train and query text generation bots built on Markov models.

### What is a Markov Model?

A Markov model is a system for predicting the next element in a sequence based
solely on the previous few entries in the sequence. This can be used to
generate text, although there is generally no guarantee that the generated text
will at all resemble the training data, other than when viewed a few words at a
time.

### How Does WebMarkov Model Text?

MarkovMerge processes textual data by first splitting it into "tokens". Web
Markov includes two tokenization schemes: "characters" and "word-not".
"Characters" straightforwardly treats every character as its own token.
"Word-not" splits tokens on word boundaries. E.g. the following text:

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

Contributors
------------

[Web Markov](https://github.com/cascadianblue/web-markov) is developed by
[Connor Boyle](https://github.com/cascadianblue).
