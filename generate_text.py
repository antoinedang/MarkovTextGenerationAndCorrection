import data.data as data
import numpy as np


unigram_probabilities = data.getUnigramProbabilities()
bigram_probabilities = data.getBigramProbabilities()
trigram_probabilities = data.getTrigramProbabilities()

def sampleWordFromProbabilities(probability_words, probability_values):
    if len(probability_words) == 0: raise ValueError
    normalized_probabilities = [p / sum(probability_values) for p in probability_values]
    random_index = np.random.choice(len(probability_words), p=normalized_probabilities)
    return list(probability_words)[random_index]

def getNextWord(words):
    if len(words) == 1:
        try: # TRY BIGRAM DISTRIBUTION
            nextWord = sampleWordFromProbabilities(bigram_probabilities[words[-1]].keys(), bigram_probabilities[words[-1]].values())
        except: # USE UNIGRAM DISTRIBUTION
            nextWord = sampleWordFromProbabilities(unigram_probabilities.keys(), unigram_probabilities.values())
    else:
        try: # TRY TRIGRAM DISTRIBUTION
            nextWord = sampleWordFromProbabilities(trigram_probabilities[words[-2]][words[-1]].keys(), trigram_probabilities[words[-2]][words[-1]].values())
        except: # USE BIGRAM or UNIGRAM DISTRIBUTIONS
            try: # TRY BIGRAM DISTRIBUTION
                nextWord = sampleWordFromProbabilities(bigram_probabilities[words[-1]].keys(), bigram_probabilities[words[-1]].values())
            except: # USE UNIGRAM DISTRIBUTIONS
                nextWord = sampleWordFromProbabilities(unigram_probabilities.keys(), unigram_probabilities.values())
                
    return nextWord
        
def generateSentence(seed=0):
    np.random.seed(seed)
    
    words = ['<s>\n']
            
    while str(words[-1]) != "</s>\n":
        words.append(getNextWord(words))
        
    output = ""    

    for word in words:
        output += word[:-1] + " "
        
    return output

print(generateSentence(0))
print(generateSentence(1))
print(generateSentence(2))
print(generateSentence(6))
print(generateSentence(15))