import spacy
from spacy.lang.en.stop_words import STOP_WORDS
from heapq import nlargest
from youtube_transcript_api import YouTubeTranscriptApi


def listToString(s):
    str1 = ""
    for ele in s:
        str1 = str1+ele+" "
    return str1

def linkToId(s):
    return s.split('/')


def allSumm(link,shrinkage):
    from string import punctuation
    ID = linkToId(link)
    shrinkage /= 100
    text = YouTubeTranscriptApi.get_transcript(ID[-1])
    #print("This is Text")
    #print(text)
    #print('\n')

    myvalues = [i['text'] for i in text if 'text' in i]
    myvalues = listToString(myvalues)
    #print("This is myvalues")
    #print(myvalues)
    #print('\n')

    #print("\n\n\n\n\n\n\n\n")

    stopwords = list(STOP_WORDS)
    nlp = spacy.load('en_core_web_sm')
    doc = nlp(myvalues)
    tokens = [token.text for token in doc]
    punctuation = punctuation + '\n'

    word_frequencies = {}
    #counting word frequency
    for word in doc:
        if word.text.lower() not in stopwords:
            if word.text.lower() not in punctuation:
                if word.text not in word_frequencies.keys():
                    word_frequencies[word.text] = 1
                else:
                    word_frequencies[word.text] += 1


    #calculating maximum frequency word
    max_frequency = max(word_frequencies.values())



    for word in word_frequencies.keys():
        word_frequencies[word] = word_frequencies[word]/max_frequency


    sentence_tokens = [sent for sent in doc.sents]


    #counting sentence frequency
    sentence_scores = {}
    for sent in sentence_tokens:
        for word in sent:
            if word.text.lower() in word_frequencies.keys():
                if sent not in sentence_scores.keys():
                    sentence_scores[sent] = word_frequencies[word.text.lower()]
                else:
                    sentence_scores[sent] += word_frequencies[word.text.lower()]
    #print('\n')
    # print("This is sentence scores:")
    # print(sentence_scores)

    select_length = int(len(sentence_tokens)*shrinkage)


    summary = nlargest(select_length,sentence_scores,key = sentence_scores.get)

    final_summary = [word.text for word in summary]
    summary = ' '.join(final_summary)
    print('\n')
    #print(summary)
    return summary

link = input("Enter link of the video:")
shrinkage = float(input("Enter percentage of reduction you want:"))
print(shrinkage)
final_text = allSumm(link,shrinkage)
print(final_text)