import data.data as data
import numpy as np
import math
from difflib import ndiff

bigram_probabilities = data.getBigramProbabilities()
vocab = data.getVocabArray()
poisson_parameter = 0.01

#SOURCE: https://codereview.stackexchange.com/questions/217065/calculate-levenshtein-distance-between-two-strings-in-python/217074#217074
def calculate_levenshtein_distance(str_1, str_2):
    """
        The Levenshtein distance is a string metric for measuring the difference between two sequences.
        It is calculated as the minimum number of single-character edits necessary to transform one string into another
    """
    distance = 0
    buffer_removed = buffer_added = 0
    for x in ndiff(str_1, str_2):
        code = x[0]
        # Code ? is ignored as it does not translate to any modification
        if code == ' ':
            distance += max(buffer_removed, buffer_added)
            buffer_removed = buffer_added = 0
        elif code == '-':
            buffer_removed += 1
        elif code == '+':
            buffer_added += 1
    distance += max(buffer_removed, buffer_added)
    return distance

def probObservationGivenState(observation, state):
    k = calculate_levenshtein_distance(observation, state)
    return ((poisson_parameter ** k) * math.exp(-k)) / math.factorial(k)

def correctSentence(sentence):
    observations = sentence.split(" ")
    probabilities = [{word: 0.0 for word in vocab[1:]} for _ in observations]
    backpointer = [{word: None for word in vocab[1:]} for _ in observations]
    
    #INITIALIZATION
    for word in vocab[1:]:
        try:
            p_word_given_first_word = bigram_probabilities['<s>\n'][word]
        except: # PROBABILITY IS 0
            p_word_given_first_word = 0
        p_emit = probObservationGivenState(observations[0], word[:-1])
        probabilities[0][word] = p_word_given_first_word * p_emit
        backpointer[0][word] = '<s>\n'
    
    for o in range(1,len(observations)):
        for word in vocab[1:]:
            progress = (vocab.index(word) + len(vocab)*(o-1)) / (len(vocab) * (len(observations) - 1))
            print("{}%...              ".format(progress*100), end='\r')
            
            p_emit = probObservationGivenState(observations[o], word[:-1])
            max_p_word_given_last_word = 0
            for last_word in probabilities[o].keys():
                p_last_word = probabilities[o-1][last_word]
                try:
                    p_word_given_last_word = bigram_probabilities[last_word][word]
                except: # PROBABILITY IS 0
                    p_word_given_last_word = 0
                p_word_given_last_word = p_word_given_last_word * p_last_word
                if max_p_word_given_last_word < p_word_given_last_word:
                    max_p_word_given_last_word = p_word_given_last_word
                    backpointer[o][word] = last_word
                    
            probabilities[o][word] = max_p_word_given_last_word * p_emit
    
    max_p_final_word = None
    p_final_word = 0
    for word, prob in probabilities[-1].items():
        if prob > p_final_word:
            p_final_word = prob
            max_p_final_word = word
    
    max_p_sentence = [max_p_final_word]
    
    backpointer.reverse()
    for backpoint_dict in backpointer:
        max_p_final_word = backpoint_dict[max_p_final_word]
        max_p_sentence = [max_p_final_word] + max_p_sentence
    
    corrected_sentence = ''
    for word in max_p_sentence:
        corrected_sentence += word[:-1] + " "
    return corrected_sentence[:-1]

sentences_to_decode = [
    "I think hat twelve thousand pounds",
    "she haf heard them",
    "She was ulreedy quit live",
    "John Knightly wasn't hard at work",
    "he said nit word by",
]

for sentence in sentences_to_decode:
    print(sentence)
    corrected = correctSentence(sentence)
    print("CORRECTED: {}".format(corrected))