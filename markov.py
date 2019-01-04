import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

from histograms import Dictogram
import random
from collections import deque
import pandas as pd
import re

def make_markov_model(data):
    markov_model = dict()
    '''
    Markov Model Structure
    A dictionary that stores windows as the key in the key-value pair and then the value for each key is a dictogram.
    A histogram of words for each window so I know what the next state can be based on a current state
    '''

    for i in range(0, len(data)-1):
        if data[i] in markov_model:
            # We have to just append to the existing histogram
            markov_model[data[i]].update([data[i+1]])
        else:
            markov_model[data[i]] = Dictogram([data[i+1]])
    return markov_model



def make_higher_order_markov_model(order, data):
	markov_model = dict()
	'''
	Nth Order Markov Model Structure
	Very similar to the first order Markov Model, but in this case we store a tuple as the key in the key-value pair in the dictionary. 
	We do this because a tuple is a great way to represent a single list. 
	And we use a tuple instead of a list because a key in a dictionary should not change and tuples are immutable. 
	'''
	for i in range(0, len(data)-order):
		# Create the window
		window = tuple(data[i: i+order])
		# Add to the dictionary
		if window in markov_model:
			# We have to just append to the existing Dictogram
			markov_model[window].update([data[i+order]])
		else:
			markov_model[window] = Dictogram([data[i+order]])
	return markov_model

def generate_random_start(model):
	# To just generate any starting word uncomment line:
	# return random.choice(model.keys())
	
	# To generate a "valid" starting word use:
	# Valid starting words are words that started a sentence in the corpus
	if 'END' in model:
		seed_word = 'END'
		while seed_word == 'END':
			seed_word = model['END'].return_weighted_random_word()
		return seed_word
	return (random.choice(list(model.keys())))


def generate_random_sentence(length, markov_model):
	current_word = generate_random_start(markov_model)
	sentence = list(current_word)

	word = list(current_word)
	word.pop(0)

	for i in range(0, length):
		current_dictogram = markov_model[current_word]
		random_weighted_word = current_dictogram.return_weighted_random_word()
		word.append(random_weighted_word)
		current_word = tuple(word)
		sentence.append(word[-1])
		word.pop(0)

	sentence[0] = sentence[0].capitalize()
	return ' '.join(sentence) + '.'
	return sentence


DIR_PATH = os.path.dirname(os.path.realpath(__file__))
FILE_NAME = "stories_english.txt"
f = open(DIR_PATH + "/Input/" + FILE_NAME)
g = open(DIR_PATH + "/Output/" + FILE_NAME, 'w')

data = f.read()
data = re.sub(r"[\n']",' ',data)
data = re.sub(r"[^\w\' '\,\-\.\"]",'',data).lower().split(' ')
#
model = make_higher_order_markov_model(2, data)

text = generate_random_sentence(150,model)
g.write(text)
print(text)
g.close()