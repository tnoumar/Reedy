import bs4 as bs #importing beautifulsoup
import urllib.request #opens and reads urls
import re #importing regex
import nltk
import PyPDF2
import textract

arg= input("Please enter the book (.pdf) you want to summarize?")
pdfFileObj = open('pdfs/'+str(arg), 'rb')
print(arg)
text = textract.process("pdfs/"+str(arg))
#scrape text from pdf



article_text = text
print(type(text))


formatted_article_text = re.sub(r'[^a-zA-Z]', ' ', article_text)
formatted_article_text = re.sub(r'\s+', ' ', formatted_article_text)
sentence_list = nltk.sent_tokenize(article_text)
stopwords = nltk.corpus.stopwords.words('english') #working with english stopwords

word_frequencies = {}
for word in nltk.word_tokenize(formatted_article_text):
    if word not in stopwords:
        if word not in word_frequencies.keys():
            word_frequencies[word] = 1
        else:
            word_frequencies[word] += 1

sorted_word_frequencies=sorted(word_frequencies.items(), key=lambda x: x[1], reverse=True)
maximum_frequncy = max(word_frequencies.values())
for word in word_frequencies.keys():
    word_frequencies[word] = (word_frequencies[word]/maximum_frequncy)

sentence_scores = {}
for sent in sentence_list:
    for word in nltk.word_tokenize(sent.lower()):
        if word in word_frequencies.keys():
            if len(sent.split(' ')) < 40:
                if sent not in sentence_scores.keys():
                    sentence_scores[sent] = word_frequencies[word]
                else:
                    sentence_scores[sent] += word_frequencies[word]
import heapq
summary_sentences = heapq.nlargest(7, sentence_scores, key=sentence_scores.get)

summary = ' '.join(summary_sentences)
print(summary)