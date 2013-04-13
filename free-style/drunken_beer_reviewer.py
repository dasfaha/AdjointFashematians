#!/usr/bin/python

""""
EXAMPLES
--------
Drunken Robo Reviewer 5000 Says...
Review: very light belgian yeasts and green bottled beers. taste either. but primarily grapefruit , and does n't smack taking a smooth experience

Drunken Robo Reviewer 5000 Says...
thick syrupy smells like a slightly buttery malt. i will continue to the smoke is wet on me , and easy to. tangerine highlights when it in a finger off with some grassy , and 1 % rating

Drunken Robo Reviewer 5000 Says...
Review: pours a bit of citrus and pirckly , with the mouth it up front. i can a super high , with a tad away. pours fresh air
"""

from nltk.tokenize import word_tokenize
from pymarkovchain import MarkovChain

def process(line):
    line = line.replace('review/text:', '')
    line = line.lower()
    return word_tokenize(line)

f = open('beeradvocate.txt', 'r')
text_data = []
name_data = []

line_count = 0

print 'Please wait, Robo reviewing 5000 is consuming beer..'

for line in f.readlines():
    if line.startswith('review/text'):
        text_data.append(process(line))
        line_count += 1
    if line_count > 2000:
        break

print 'Drunken Robo Reviewer 5000 Says...'
MarkovChain().generateDatabase(' '.join(sum(text_data, [])))
print 'Review:', '. '.join([MarkovChain().generateString() for i in range(3)])


