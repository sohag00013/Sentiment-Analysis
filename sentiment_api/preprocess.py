
#https://kavita-ganesan.com/what-are-stop-words/
#https://github.com/igorbrigadir/stopwords/blob/master/en/terrier.txt
#https://www.opinosis-analytics.com/knowledge-base/stop-words-explained/
import unidecode
import pandas as pd
import re
import time
import nltk
from nltk.corpus import stopwords
nltk.download('stopwords')
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from autocorrect import Speller
from bs4 import BeautifulSoup
from nltk.corpus import stopwords
from nltk import word_tokenize
import string
import timeit

CONTRACTION_MAP = {
"ain't": "is not",
"aren't": "are not",
"can't": "cannot",
"can't've": "cannot have",
"'cause": "because",
"could've": "could have",
"couldn't": "could not",
"couldn't've": "could not have",
"didn't": "did not",
"doesn't": "does not",
"don't": "do not",
"hadn't": "had not",
"hadn't've": "had not have",
"hasn't": "has not",
"haven't": "have not",
"he'd": "he would",
"he'd've": "he would have",
"he'll": "he will",
"he'll've": "he he will have",
"he's": "he is",
"how'd": "how did",
"how'd'y": "how do you",
"how'll": "how will",
"how's": "how is",
"i'd": "i would",
"i'd've": "i would have",
"i'll": "i will",
"i'll've": "i will have",
"i'm": "i am",
"i've": "i have",
"isn't": "is not",
"it'd": "it would",
"it'd've": "it would have",
"it'll": "it will",
"it'll've": "it will have",
"it's": "it is",
"let's": "let us",
"ma'am": "madam",
"mayn't": "may not",
"might've": "might have",
"mightn't": "might not",
"mightn't've": "might not have",
"must've": "must have",
"mustn't": "must not",
"mustn't've": "must not have",
"needn't": "need not",
"needn't've": "need not have",
"o'clock": "of the clock",
"oughtn't": "ought not",
"oughtn't've": "ought not have",
"shan't": "shall not",
"sha'n't": "shall not",
"shan't've": "shall not have",
"she'd": "she would",
"she'd've": "she would have",
"she'll": "she will",
"she'll've": "she will have",
"she's": "she is",
"should've": "should have",
"shouldn't": "should not",
"shouldn't've": "should not have",
"so've": "so have",
"so's": "so as",
"that'd": "that would",
"that'd've": "that would have",
"that's": "that is",
"there'd": "there would",
"there'd've": "there would have",
"there's": "there is",
"they'd": "they would",
"they'd've": "they would have",
"they'll": "they will",
"they'll've": "they will have",
"they're": "they are",
"they've": "they have",
"to've": "to have",
"wasn't": "was not",
"we'd": "we would",
"we'd've": "we would have",
"we'll": "we will",
"we'll've": "we will have",
"we're": "we are",
"we've": "we have",
"weren't": "were not",
"what'll": "what will",
"what'll've": "what will have",
"what're": "what are",
"what's": "what is",
"what've": "what have",
"when's": "when is",
"when've": "when have",
"where'd": "where did",
"where's": "where is",
"where've": "where have",
"who'll": "who will",
"who'll've": "who will have",
"who's": "who is",
"who've": "who have",
"why's": "why is",
"why've": "why have",
"will've": "will have",
"won't": "will not",
"won't've": "will not have",
"would've": "would have",
"wouldn't": "would not",
"wouldn't've": "would not have",
"y'all": "you all",
"y'all'd": "you all would",
"y'all'd've": "you all would have",
"y'all're": "you all are",
"y'all've": "you all have",
"you'd": "you would",
"you'd've": "you would have",
"you'll": "you will",
"you'll've": "you will have",
"you're": "you are",
"you've": "you have",
}


def remove_newlines_tabs(text):
    # #if(re.match('\\n\n\t\\. com.com',text)):
    # if(re.search('\\n'))
    # Formatted_text = text.replace('\\n', ' ')
    Formatted_text = text.replace('\\n', ' ').replace('\n', ' ').replace('\t',' ').replace('\\', ' ').replace('. com', '.com')
    return Formatted_text

def strip_html_tags(text):
    soup = BeautifulSoup(text, "html.parser")
    stripped_text = soup.get_text(separator=" ")
    return stripped_text

def remove_links(text):
    remove_https = re.sub(r'http\S+', '', text)
    remove_com = re.sub(r"\ [A-Za-z]*\.com", " ", remove_https)
    return remove_com

def remove_whitespace(text):
    pattern = re.compile(r'\s+')
    Without_whitespace = re.sub(pattern, ' ', text)
    text = Without_whitespace.replace('?', ' ? ').replace(')', ') ')
    return text

def accented_characters_removal(text):
    text = unidecode.unidecode(text)
    return text

# Code for text lowercasing
def lower_casing_text(text):
    text = text.lower()
    return text

def reducing_incorrect_character_repeatation(text):
    Pattern_alpha = re.compile(r"([A-Za-z])\1{1,}", re.DOTALL)
    Formatted_text = Pattern_alpha.sub(r"\1\1", text)
    Pattern_Punct = re.compile(r'([.,/#!$%^&*?;:{}=_`~()+-])\1{1,}')
    Combined_Formatted = Pattern_Punct.sub(r'\1', Formatted_text)
    Final_Formatted = re.sub(' {2,}',' ', Combined_Formatted)
    return Final_Formatted

def expand_contractions(text, contraction_mapping =  CONTRACTION_MAP):
    list_Of_tokens = text.split(' ')
    for Word in list_Of_tokens:
         if Word in CONTRACTION_MAP:
                list_Of_tokens = [item.replace(Word, CONTRACTION_MAP[Word]) for item in list_Of_tokens]
    String_Of_tokens = ' '.join(str(e) for e in list_Of_tokens)
    return String_Of_tokens

def removing_special_characters(text):
    Formatted_Text = re.sub(r"[^a-zA-Z0-9$-,%.?!]+", ' ', text)
    return Formatted_Text

def spelling_correction(text):
    spell = Speller(lang='en')
    Corrected_text = spell(text)
    return Corrected_text


def text_preprocess(text):
    text = remove_newlines_tabs(text)
    text = strip_html_tags(text)
    text = remove_links(text)
    text = remove_whitespace(text)
    text = accented_characters_removal(text)
    text = lower_casing_text(text)
    text = reducing_incorrect_character_repeatation(text)
    text = expand_contractions(text, contraction_mapping =  CONTRACTION_MAP)
    text = removing_special_characters(text)
    text = spelling_correction(text)
    return text
    

# text="This is herrrrrrrrrrrrr can't \\ first day K-a-j-a-l. Thi*s is $100.05 at this place.\n Please,\t Be nice to her.\\n"

# print("%%%%%%%%%%%%%%%%%%%%%%%%% : ",text_preprocess(text))

