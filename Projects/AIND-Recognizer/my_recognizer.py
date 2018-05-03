import warnings
import arpa
from asl_data import SinglesData


def recognize(models: dict, test_set: SinglesData):
    """ Recognize test word sequences from word models set

   :param models: dict of trained models
       {'SOMEWORD': GaussianHMM model object, 'SOMEOTHERWORD': GaussianHMM model object, ...}
   :param test_set: SinglesData object
   :return: (list, list)  as probabilities, guesses
       both lists are ordered by the test set word_id
       probabilities is a list of dictionaries where each key a word and value is Log Liklihood
           [{SOMEWORD': LogLvalue, 'SOMEOTHERWORD' LogLvalue, ... },
            {SOMEWORD': LogLvalue, 'SOMEOTHERWORD' LogLvalue, ... },
            ]
       guesses is a list of the best guess words ordered by the test set word_id
           ['WORDGUESS0', 'WORDGUESS1', 'WORDGUESS2',...]
   """
    warnings.filterwarnings("ignore", category=DeprecationWarning)
    probabilities = []
    guesses = []
    # TODO implement the recognizer
    # return probabilities, guesses
    for _, (X, lengths) in test_set.get_all_Xlengths().items():
        prob_dict = {}
        max_log_likelihood = float('-inf')
        guess = None

        for word, model in models.items():
            try:
                log_likelihood = model.score(X, lengths)
                prob_dict[word] = log_likelihood

                if log_likelihood > max_log_likelihood:
                    max_log_likelihood = log_likelihood
                    guess = word
            except:
                prob_dict[word] = float('-inf')
        
        probabilities.append(prob_dict)
        guesses.append(guess)

    return probabilities, guesses

def recognize_with_language_model(models: dict, test_set: SinglesData, language_model: arpa.models.simple.ARPAModelSimple):
    """ Recognize test word sequences from word models set

   :param models: dict of trained models
       {'SOMEWORD': GaussianHMM model object, 'SOMEOTHERWORD': GaussianHMM model object, ...}
   :param test_set: SinglesData object
   :return: (list, list)  as probabilities, guesses
       both lists are ordered by the test set word_id
       probabilities is a list of dictionaries where each key a word and value is Log Liklihood
           [{SOMEWORD': LogLvalue, 'SOMEOTHERWORD' LogLvalue, ... },
            {SOMEWORD': LogLvalue, 'SOMEOTHERWORD' LogLvalue, ... },
            ]
       guesses is a list of the best guess words ordered by the test set word_id
           ['WORDGUESS0', 'WORDGUESS1', 'WORDGUESS2',...]
   """
    warnings.filterwarnings("ignore", category=DeprecationWarning)
    probabilities = []
    guesses = []
    f = open('record.txt', 'a+')
    
    for k in sorted(test_set.sentences_index):
        items = test_set.sentences_index[k]
        first_word = None
        second_word = None
        top_5_sentences = []
        top_5_guesses = []
        for i in range(5):
            top_5_guesses.append([None, float('-inf')])

        for i in range(len(items)):
            prob_dict = {}
            X, lengths = test_set.get_item_Xlengths(items[i])

            if i == 0:
                for word, model in models.items():
                    try:
                        log_likelihood = model.score(X, lengths)
                        prob_dict[word] = log_likelihood
                    except:
                        prob_dict[word] = float('-inf')

                probabilities.append(prob_dict)
                
                sorted_by_value = [k for k in sorted(prob_dict, key = prob_dict.get, reverse = True)]
                for k in sorted_by_value[:5]:
                    top_5_sentences.append([['<s>', k], prob_dict[k]])
            else:
                for word, model in models.items():
                    log_likelihood = None
                    try:
                        log_likelihood = model.score(X, lengths)
                    except:
                        log_likelihood = float('-inf')
                    
                    prob_dict[word] = log_likelihood

                    for j in range(5):
                        first_word = top_5_sentences[j][0][-2]
                        second_word = top_5_sentences[j][0][-1]

                        lm_log_p = None
                        try:
                            lm_log_p = language_model.log_p("{} {} {}".format(first_word, second_word, word))
                        except:
                            lm_log_p = -99.0

                        combined_log_p = 20.0 * lm_log_p + log_likelihood + top_5_sentences[j][1]

                        if combined_log_p > top_5_guesses[j][1]:
                            top_5_guesses[j][0] = word
                            top_5_guesses[j][1] = combined_log_p

                probabilities.append(prob_dict)

                for j in range(5):
                    top_5_sentences[j][0].append(top_5_guesses[j][0])
                    top_5_sentences[j][1] = top_5_guesses[j][1]
                    top_5_guesses[j] = [None, float('-inf')]
            
            for j in range(5):
                f.write("{}\r\n".format(top_5_sentences[j]))
            
            f.write("\r\n")

        top_sentence = sorted(top_5_sentences, key = lambda s : s[1], reverse = True)[0]
        guesses.extend(top_sentence[0][1:])
    
    f.close()
                    
    return probabilities, guesses
