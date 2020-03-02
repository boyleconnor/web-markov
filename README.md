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
solely on the previous few entries in the sequence. Markov models have found
many applications

### How Does MarkovMerge Model Text?

MarkovMerge first processes textual data by first splitting it along word
boundaries. Unlike some other text-prediction Markov models, MarkovMerge treats
the punctuation and whitespace in between words as data of equal importance to
the words themselves. E.g. the following text:

~~~~~
"Hello, how are you?"
~~~~~

will be split into the following tokens:

~~~~
"Hello" + ", " + "how" + " " + "are" + " " + "you" + "?"
~~~~

if the user has chosen an n-gram size of 4, then occurrences of tokens will be counted 4 tokens at a time:

~~~~
"Hello" + ", " + "how"  -> " "
", " + "how" + " "      -> "are"
~~~~

etc. until the end of the text.


### How Does MarkovMerge Create Erratic Texts?

The script, which is a proof of concept, trains two markov models, each based
on a different source. Then, it creates a third markov model which is a fusion
of two. The fused model is used to generate several (thousands+) texts. Each of
these texts' constituent n-grams is marked positively with a positive
probability (0.0 <= p <= 1.0) if it is found often in one source, added to a
negative probability if it is found often in the other source. The texts are
then sorted by the difference between the max and min of this value within the
text.

The end goal is to generate texts that sound distinctly like one source in
parts, and distinctly like the other source in other parts.
