import os
import nltk
import  string
import random
import warnings
import wikipedia
import numpy as np
from nltk import word_tokenize
from chatterbot import ChatBot
warnings.filterwarnings("ignore")
from nltk.corpus import stopwords
from nltk.chat.util import Chat, reflections
from validate_email import validate_email
from chatterbot.trainers import ListTrainer
from sklearn.metrics.pairwise import cosine_similarity
from chatterbot.trainers import ChatterBotCorpusTrainer
from sklearn.feature_extraction.text import TfidfVectorizer


def greeting(sentence):
        for word in sentence.split():
                if word.lower() in greeting_inputs:
                        return random.choice(greeting_responses)

def thank_u(sentence):
        for word in sentence.split():
                if word.lower() in thank_you:
                        return random.choice(thank_you)

def noo(sentence):
        for word in sentence.split():
                if word.lower() in no:
                        return random.choice(no)
                    
def k_s(sentence):
        for word in sentence.split():
                if word.lower() in ok_yes:
                        return random.choice(ok_yes)

