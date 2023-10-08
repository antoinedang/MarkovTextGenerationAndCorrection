import data
import numpy as np

bigram_probabilities = data.getBigramProbabilities()
vocab = data.getVocabArray()
poisson_parameter = 0.01


def getEditDistance(str1, str2):
    return 0

def correctSentence(words):
    pass

def probObservationGivenState(observation_word, ):

def viterbi(obs):
    num_states = len(obs)
    
    # Initialize the Viterbi matrix and the backpointer matrix
    viterbi_matrix = np.zeros((num_states, num_states))
    backpointer = np.zeros((num_states, num_states), dtype=int)
    
    # Initialize the first column of the Viterbi matrix
    for word, prob in bigram_probabilities["<s>\n"].items():
        word_i = vocab.index(word)
        viterbi_matrix[word_i, 0] = prob
    
    # Forward pass: Fill in the Viterbi matrix
    for t in range(1, n):
        for s in range(m):
            trans_prob_s = viterbi_matrix[:, t - 1] * trans_prob[:, s]
            max_trans_prob = np.max(trans_prob_s)
            viterbi_matrix[s, t] = max_trans_prob * emit_prob[s, obs[t]]
            backpointer[s, t] = np.argmax(trans_prob_s)
    
    # Termination: Find the best final state
    best_final_state = np.argmax(viterbi_matrix[:, -1])
    
    # Backtrack to find the best path
    best_path = [best_final_state]
    for t in range(n - 1, 0, -1):
        best_final_state = backpointer[best_final_state, t]
        best_path.insert(0, best_final_state)
    
    return best_path


words_to_correct = ["I", "think", "hat", "twelve", "thousand", "pounds"]
print(words_to_correct)
print(correctSentence(words_to_correct))
