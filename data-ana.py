import time
import matplotlib.pyplot as plt
import numpy as np
from collections import Counter
from datetime import datetime
import re
import pandas as pd

def FindAuthor(s):
    patterns = [
        '- ([\w]+): ',                        # First Name
        '- ([\w]+[\s]+[\w]+): ',              # First Name + Last Name
        '- ([\w]+[\s]+[\w]+[\s]+[\w]+): ',    # First Name + Middle Name + Last Name
        '- ([+]\d{2} \d{5} \d{5}): ',         # Mobile Number (India)
        '- ([+]\d{2} \d{3} \d{3} \d{4}): ',   # Mobile Number (US)
        '- ([+]\d{2} \d{4} \d{7})'           # Mobile Number (Europe)
    ]
    pattern = '|'.join(patterns)
    result = re.search(pattern, s)
    if result:
        return result.group()
    else:
        print('author not found')
        return False

def FindDate(s):
    pattern = '^(([0-9]|10|11|12))(\/)([0-2][0-9]|(3)[0-1]|[1-9])(\/)(\d{2}|\d{4}), ([0-9][0-9]):([0-9][0-9]) -'
    result = re.search(pattern, s)
    if result:
        return result.group()
    else:
        return False

def GetData(title,lines_to_skip):
    message_set = []
    author_message_set = []
    date_message_set = []
    with open(title, 'r') as f:
        data = f.read().split('\n')
    for index, line in enumerate(data):
        if index < lines_to_skip:
            print("Non-message line: {}".format(line))
            continue
        else:
            date = FindDate(line)
            if date:
                author = FindAuthor(line)
                author = author.replace('- ','')
                message1 = line.replace(date,'')
                message = message1.replace(author,'')
                message_set.append(message)
                date_message_set.append(date.replace(' -',''))
                author_message_set.append(author.replace(': ',''))
            else: #Add line to previous message
                message_set[-1] = message_set[-1] + line

    return message_set, author_message_set, date_message_set

def runit(title,num):
    m, a, d = GetData(title,num)
    return m, a, d

def Analyze_Date(message_set, author_message_set, date_message_set):
    author_set = list(set(author_message_set))
    num_chars = []
    num_mess = []
    num_words = []
    big_messages = 0
    num_words_per_mess = []
    num_chars_per_word = []

    for a_ind,author in enumerate(author_set):
        num_chars.append(0)
        num_words.append(0)
        num_mess.append(0)
        num_words_per_mess.append([])
        num_chars_per_word.append([])

        for m_ind,mess in enumerate(message_set):
            if author_message_set[m_ind] == author_set[a_ind]:
                num_chars_in_mess = len(mess)
                num_words_in_mess = len(mess.split(" "))
                if num_chars_in_mess > 5000:
                    big_messages += 1
                    continue
                else:

                    for word in mess.split(" "):
                        #print(word)
                        #print(len(word))
                        if len(word) > 0:
                            num_chars_per_word[a_ind].append(len(word))
                        #print(num_chars_per_word)
                        #input('continue')
                    num_chars[a_ind] += num_chars_in_mess
                    num_words[a_ind] += num_words_in_mess
                    num_mess[a_ind] += 1
                    num_words_per_mess[a_ind].append(num_words_in_mess)

    return author_set, num_chars, num_words, num_mess, num_words_per_mess, num_chars_per_word

def Plotting(author_set, plot_char_dist, plot_word_dist):
    colors = ["red","green","blue"]
    upper_range = 50

    plt.style.use('seaborn-deep')

    bins = np.linspace(0,upper_range,upper_range)
    plt.hist(plot_word_dist, bins, label=author_set, density=True)#,alpha=0.3)
    plt.ylabel('Probability');
    plt.legend(loc='upper right')
    plt.title('Word Distribution of author_message_set')
    plt.xlim([1,upper_range])
    plt.show()

    upper_range = 20
    bins = np.linspace(0,upper_range,upper_range)
    plt.hist(plot_char_dist, bins, label=author_set, density=True)#,alpha=0.3)
    plt.ylabel('Probability');
    plt.legend(loc='upper right')
    plt.title('Char Distribution of author_message_set')
    #plt.xlim([0,upper_range])
    plt.show()

test = '3/19/20, 18:30 - Bobby: Nature boy   '
fthisapp = 'fthisapp.txt.txt'
test2 = 'test2.txt'
jen = 'ken.txt'

##title, num = fthisapp, 3
#title, num = test2, 0
#title, num = jen, 1
title, num = 'mom.txt', 3

message_set, author_message_set, date_message_set = runit(title,num)

author_set, num_chars, num_words, num_mess, num_words_per_mess, num_chars_per_word = Analyze_Date(message_set, author_message_set, date_message_set)

plot_word_dist = []
plot_char_dist = []
upper_range = 50

for ind,auth in enumerate(author_set):
    num_word_dist = num_words_per_mess[ind]
    for n_ind,num in enumerate(num_word_dist):
        if num > upper_range:
            num_word_dist[n_ind] = upper_range

    plot_word_dist.append(num_word_dist)

    print("{}: {} chars per word, {} words per text, {} texts total".format(auth,
            num_chars[ind]/num_words[ind],num_words[ind]/num_mess[ind],
            num_mess[ind]))

Plotting(author_set, num_chars_per_word, plot_word_dist)


"""
someone to laugh with (haha- 1000 occurrences)
talk to any time
gym buddies
gifs (media omitted)

wrap whatsapp into messages, format into github, put tasks aright - make histograms, etc.
words per text distribution in Meh histogram - do this tomorrow

Time distribution of texts over time
Clean up output stats and wrap into function
Most common words
Time distribution of text messages by Day
Time distribution of text messages by Time
"""
