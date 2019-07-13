"""
THIS PROGRAM AIMS TO IMPLEMENT SENTIMENT ANALYSIS
USING PYTHON PROGRAMMING LANGUAGE
It receives a line of text as input and the polarity of the text
i.e. positive, negative or neutral is returned as output
"""

__authors__ = ["Anu Mary Abey" , "Athena E."]

__version__ = [1]

# function definition

def remove_stop_words(list_of_words):
    """Returns a list of words from which
    the stop words have been removed"""
    
    with open("stop_words.txt","Ur") as file_of_stop_words:
        collection_of_stop_words = file_of_stop_words.read()
    
    collection_of_stop_words = collection_of_stop_words.split("\n")
    
    # delete stop words to save on execution time
    list_of_words = [word for word in list_of_words if word.lower() not in collection_of_stop_words]
    
    return list_of_words


def determine_positive_polarity(list_of_words):
    """Returns a tuple containing
    the positive polarity, no. of positive words,
    collection of positive words"""
    
    polarity = 0.0
    no_of_positive_words = 0

    with open("positive_words.txt","Ur") as file_of_positive_words:
        collection_of_positive_words = file_of_positive_words.read()
    collection_of_positive_words = collection_of_positive_words.split("\n")

    with open("decremental_words.txt","Ur") as file_of_decremental_words:
        collection_of_decremental_words = file_of_decremental_words.read()
    collection_of_decremental_words = collection_of_decremental_words.split("\n")
    
    for i in range(len(list_of_words)):
        word = list_of_words[i]
        previous_word = list_of_words[i-1]
        if word.lower() in collection_of_positive_words:
            if previous_word.lower() in collection_of_decremental_words:
                polarity -= 1
            else:
                polarity += 1
            no_of_positive_words += 1

    return polarity,no_of_positive_words,collection_of_positive_words

def determine_negative_polarity(list_of_words):
    """Returns a tuple containing
    the positive polarity, no. of negative words,
    collection of negative words"""
    
    polarity = 0.0
    no_of_negative_words = 0
    
    with open("negative_words.txt","Ur") as file_of_negative_words:
        collection_of_negative_words = file_of_negative_words.read()
    collection_of_negative_words = collection_of_negative_words.split("\n")

    with open("decremental_words.txt","Ur") as file_of_decremental_words:
        collection_of_decremental_words = file_of_decremental_words.read()
    collection_of_decremental_words = collection_of_decremental_words.split("\n")
    
    for i in range(len(list_of_words)):
        word = list_of_words[i]
        previous_word = list_of_words[i-1]
        if word.lower() in collection_of_negative_words:
            if previous_word.lower() in collection_of_decremental_words:
                polarity += 1
            else:
                polarity -= 1
            no_of_negative_words += 1

    return polarity,no_of_negative_words,collection_of_negative_words

def increment_and_decrement_polarity(list_of_words,collection_of_positive_words,collection_of_negative_words):
    """Returns the polarity of a sentence
        after considering any words that heighten
        the polarity of the text"""
    
    polarity = 0.0

    with open("incremental_words.txt","Ur") as file_of_incremental_words:
        collection_of_incremental_words = file_of_incremental_words.read()
    with open("decremental_words.txt","Ur") as file_of_decremental_words:
        collection_of_decremental_words = file_of_decremental_words.read()

    collection_of_incremental_words = collection_of_incremental_words.split("\n")
    collection_of_decremental_words = collection_of_decremental_words.split("\n")

    for i in range(len(list_of_words)):
        # if an incremental word is found:
        # add 2 to the polarity if the combination of words heightens positive polarity
        # subtract 2 from the polarity if the combination of words heightens negative polarity
        if list_of_words[i] in collection_of_incremental_words:
            if list_of_words[i+1] in collection_of_positive_words:
                polarity += 2

            elif list_of_words[i+1] in collection_of_negative_words:
                polarity -= 2
        # if a decremental word is found:
        # add 2 to the polarity if the combination of words heightens negative polarity
        # subtract 2 from the polarity if the combination of words heightens positive polarity
        # because decremental words negate the meaning of phrase combinations
        # i.e. they invert the polarity
        elif list_of_words[i] in collection_of_decremental_words:
            if list_of_words[i+1] in collection_of_positive_words:
                polarity -= 2
            elif list_of_words[i+1] in collection_of_negative_words:
                polarity += 2
    return polarity

def determine_polarity_of_a_sentence(sentence):
    """Returns the polarity of a sentence along with
        the number of positive and negative words"""

    list_of_words = sentence.split()                #delimiter = whitespace 
    list_of_words = remove_stop_words(list_of_words)
    positive_polarity,no_of_positive_words,collection_of_positive_words = determine_positive_polarity(list_of_words)

    negative_polarity,no_of_negative_words,collection_of_negative_words = determine_negative_polarity(list_of_words)
    incremented_and_decremented_polarity = increment_and_decrement_polarity(list_of_words,collection_of_positive_words,collection_of_negative_words)
    polarity = positive_polarity + negative_polarity + incremented_and_decremented_polarity
    return (polarity,no_of_positive_words,no_of_negative_words)

def polarity_weightage(details):
    """Returns the polarity weightage of the paragraph"""

    net_polarity_of_paragraph = 0.0
    net_no_of_positive_words_in_the_paragraph = 0
    net_no_of_negative_words_in_the_paragraph = 0
    sentence_no = sorted(details.keys())

    for sentence in sentence_no:
        polarity_details = details[sentence]
        polarity_of_sentence = polarity_details[0]
        net_polarity_of_paragraph += polarity_of_sentence
        no_of_positive_words = polarity_details[1]
        net_no_of_positive_words_in_the_paragraph += no_of_positive_words
        no_of_negative_words = polarity_details[2]
        net_no_of_negative_words_in_the_paragraph += no_of_negative_words
    total_words = net_no_of_positive_words_in_the_paragraph + net_no_of_negative_words_in_the_paragraph
    
    if total_words == 0:
        return 0,0,0
    
    polarity = net_polarity_of_paragraph / total_words
    
    return polarity, net_no_of_positive_words_in_the_paragraph, net_no_of_negative_words_in_the_paragraph
                

# main program

# importing necessary modules
import re

# print welcome message
print "\nWelcome to Python Sentiment Analysis !\n"
print """
This program receives a line of text as input and the polarity of the text
i.e. positive, negative or neutral is displayed.
"""

# initialization
polarity = 0.0

# input
paragraph_of_text = raw_input("Please enter a paragraph of text whose polarity must be checked: ")

# compute the length of the entire text
length_of_paragraph_of_text = len(paragraph_of_text)
if length_of_paragraph_of_text == 0:
    print "Invalid entry. Please enter some text & try running this program again"
    exit()

# replace all the common abbreviations
paragraph_of_text = paragraph_of_text.replace("n't"," not")
paragraph_of_text = paragraph_of_text.replace("'m"," am")
paragraph_of_text = paragraph_of_text.replace("'re"," are")

# replace common punctuation marks i.e. '.' and "!" by newline character to split into sentences
paragraph_of_text = re.sub(re.compile("[.!?]"),'\n',paragraph_of_text)
paragraph_of_text = re.sub(re.compile("""[,"/;]"""),'',paragraph_of_text)

# split the paragraph into sentences using "\n" as the delimiter
list_of_sentences = paragraph_of_text.split("\n")

# remove all the empty strings created due to the presence of newline escape sequence
list_of_sentences = [sentence for sentence in list_of_sentences if sentence != '' ]


# polarity calculator

details = {}
# details will store sentence no, calculated polarity value, no. of positive & negative words respectively
count = 1
# calculate polarity
for sentence in list_of_sentences:
    polarity = determine_polarity_of_a_sentence(sentence)
    details['sentence'+str(count)] = polarity
    count +=1

# weight the polarity
paragraph_polarity = polarity_weightage(details)
polarity,net_no_of_positive_words_in_the_paragraph,net_no_of_negative_words_in_the_paragraph = paragraph_polarity

# sentiment analysis
if polarity > 0:
    print "The text denotes positive emotional status! :)"
elif polarity < 0:
    print "The text denotes negative emotional status! :("
elif polarity == 0:
    if net_no_of_positive_words_in_the_paragraph > net_no_of_negative_words_in_the_paragraph:
        print "The text has neutral polarity but hints positive emotional status"
    elif net_no_of_positive_words_in_the_paragraph < net_no_of_negative_words_in_the_paragraph:
        print  "The text has neutral polarity but hints negative emotional status"
    else:
        print "The text denotes neutral mood!"

# end of program
