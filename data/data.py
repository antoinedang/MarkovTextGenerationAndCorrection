def getVocabArray():
    vocab = ['']
    with open("data/vocab.txt") as f:
        for line in f.readlines():
            _, word = line.split(" ")
            vocab.append(word)
    return vocab

def getUnigramProbabilities():
    vocab = getVocabArray()
    probs = {}
    with open("data/unigram_counts.txt") as f:
        for line in f.readlines():
            word_id, log_prob = line.split(" ")
            probs[vocab[int(word_id)]] = 10 ** float(log_prob)
    return probs

def getBigramProbabilities():
    vocab = getVocabArray()
    probs = {}
    with open("data/bigram_counts.txt") as f:
        for line in f.readlines():
            word_i, word_j, log_prob = line.split(" ")
            try:
                probs[vocab[int(word_i)]][vocab[int(word_j)]] = 10 ** float(log_prob)
            except:
                probs[vocab[int(word_i)]] = {}
                probs[vocab[int(word_i)]][vocab[int(word_j)]] = 10 ** float(log_prob)
                
    return probs

def getTrigramProbabilities():
    vocab = getVocabArray()
    probs = {}
    with open("data/trigram_counts.txt") as f:
        for line in f.readlines():
            word_i, word_j, word_k, log_prob = line.split(" ")
            try:
                probs[vocab[int(word_i)]][vocab[int(word_j)]][vocab[int(word_k)]] = 10 ** float(log_prob)
            except:
                try:
                    probs[vocab[int(word_i)]][vocab[int(word_j)]] = {}
                except:
                    probs[vocab[int(word_i)]] = {}
                    probs[vocab[int(word_i)]][vocab[int(word_j)]] = {}
                probs[vocab[int(word_i)]][vocab[int(word_j)]][vocab[int(word_k)]] = 10 ** float(log_prob)
                
    return probs