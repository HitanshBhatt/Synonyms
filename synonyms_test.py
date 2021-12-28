'''Semantic Similarity: starter code

Author: Michael Guerzhoy. Last modified: Nov. 14, 2016.
'''
import math

# Don't change
def norm(vec):
    '''Return the norm of a vector stored as a dictionary,
    as described in the handout for Project 3.
    '''
    sum_of_squares = 0.0  
    for i in vec:
        sum_of_squares += vec[i] * vec[i]
    
    sum = math.sqrt(sum_of_squares)
    return sum

# Returns the cosine similarity between input vectors vec1, and vec2 stored as dictionaries (Note to self: Should be similar to norm(vec) in terms of logic and structure)
def cosine_similarity(vec1, vec2):
    num = 0.0
    for i in vec1:
        if i in vec2:                                    # Checks to see if the same key is in vec2, i.e keys in vec2 == True
            num += vec1[i]*vec2[i]                    # Incrementing the numerator 

    denom = (norm(vec1)*norm(vec2))
    return (num/denom)


# Creates a dictonary of each word itself (Note to self: Make sure complexity: O(n^2), where n is the number of words in the 'sentences' list. Otherwise, program won't run) 
def build_semantic_descriptors(sentences):
    dictionary = {}
    
    for s in sentences:
        check = []                                           # List to store the words that have not been checked
        for w in s:
            if (w not in check):                             # if the current word is not in the empty 'check' list (first iteration)
                if (w not in dictionary):                    # if the current word is not in empty dictionary, d (first iteration)
                    dictionary[w] = {}                       # Creating a new dictionary of the word itself which represents the semantic descriptor of the word
                check2 = []                                  # Another updated list to store the words that have not been checked
                for i in s:
                    if i not in check2:
                        if i!= w:                            # If i does not equalt to the current word
                            if i not in dictionary[w]:       # If i is not in d[w] (has not been checked yet)
                                dictionary[w][i] = 0         # Set the value of that word (i) to zero since it is not present in the dictionary of words
                            dictionary[w][i] += 1            #Incrementing the count of the value in the dictionary if more similar words are found
                            check2.append(i)
                check.append(w)
    #print('Check:', check)                                  # For debugging
    #print('Check 2:', check2)                               # For debugging
    return dictionary

def modify_text_from_files(collective_text):
    # For symbols that terminate a sentence, replace each symbol with a period (i.e, '.') to make reading the file easier
    collective_text = collective_text.replace('!', '.')
    collective_text = collective_text.replace("?", ".")

    # For symbols that do not terminate the sentence, but are a part of the sentence - replace with a space (i.e, ' ') 
    collective_text = collective_text.replace(",", " ")
    collective_text = collective_text.replace("-", " ")
    collective_text = collective_text.replace(";", " ")
    collective_text = collective_text.replace(":", " ")
    collective_text = collective_text.replace("--", " ")
    collective_text = collective_text.replace("\n", " ")    # Replace a new line with a space


    collective_text = collective_text.split('.')

    return collective_text

def build_semantic_descriptors_from_files(filenames):       # Note that 'filenames' is not a single file but is a list of the names of multiple files
    '''
    Possible Symbols in the file: '.', '!', '?', ',', '-', '--', ':', ';'
    '''
    collective_text = ''                                    #A string that will store text from all the files as required by the Project 3 instructions

    #To access all files, a for loop can be used to iterate through the files: filenames[0], filenames[1], filenames[2], .... , filenames[n]
    for name in range(len(filenames)):
        collective_text += open(filenames[name], "r", encoding="latin1").read()
        collective_text = collective_text.lower()
        collective_text += ' '                              # Adds a space after every iteration

    final_text = modify_text_from_files(collective_text)

    sentences = []                                          # A list to store sentences from collective_text to pass as an argument to def build_semantic_descriptors(sentences)
    for i in range(len(final_text)-1):                 # Gives index out of range error if I don't do -1
        text = final_text[i].split(' ')
        sentences.append(text)

    #To remove random spaces:
    for words in sentences:
        for letters in words:
            while '' in words:      #While there is random space
                words.remove('')

    dictionary = {}
    dictionary = build_semantic_descriptors(sentences)

    return dictionary


def most_similar_word(word, choices, semantic_descriptors, similarity_fn):
    similarity = False
    #prev_simialrity = False
    similarity_val = 0
    #prev_simialrity_val = 0
    w = word.lower()
    temp_similarity = 0
    most_similar_word = []
    final_word = ""

    for i in range(len(choices)):
        choices[i] = choices[i].lower()
    #print(choices)
    if w not in semantic_descriptors:
        return choices[0]
    
    for sem in range(len(choices)):
        if choices[sem] not in semantic_descriptors:
            similarity = False
            similarity_val = -1
        elif choices[sem] in semantic_descriptors:
            similarity_val = similarity_fn(semantic_descriptors[w], semantic_descriptors[choices[sem]])
        
        if sem == 0:
            similarity == True
            temp_similarity = similarity_val
        
        if similarity_val > temp_similarity:
            similarity = True
            temp_similarity = similarity_val
            #similarity_val = temp_similarity            #Repetitive?
            final_word = choices[sem]
    ''' most_similar_word.append(choices[sem])
        
        if len(most_similar_word) == 1:
            final_word = most_similar_word[0]
        else:
            final_word = most_similar_word[0]

    return final_word'''
    return final_word


def run_similarity_test(filename, semantic_descriptors, similarity_fn):
    file = open(filename, "r", encoding="latin1").read()
    store = []
    count = 0.0
    for text in file:
        if text!= '':
            store.append(text)

    for test in store:
        if most_similar_word(test[0], test[2:], semantic_descriptors, similarity_fn) == test[1]:
            count += 1
    
    denom = len(list)
    return (count/denom)*100.0

if __name__ == '__main__':
    print(cosine_similarity({"a": 1, "b": 2, "c": 3}, {"b": 4, "c": 5, "d": 6}))            # Should reutrn ~ 0.70 (as a float)
    print(build_semantic_descriptors([["i", "am", "a", "sick", "man"],
    ["i", "am", "a", "spiteful", "man"],
    ["i", "am", "an", "unattractive", "man"],
    ["i", "believe", "my", "liver", "is", "diseased"],
    ["however", "i", "know", "nothing", "at", "all", "about", "my",
    "disease", "and", "do", "not", "know", "for", "certain", "what", "ails", "me"]]))

    sem_descriptors = build_semantic_descriptors_from_files(["wp.txt", "sw.txt"])
    res = run_similarity_test("test.txt", sem_descriptors, cosine_similarity)
    print(res, "of the guesses were correct")
