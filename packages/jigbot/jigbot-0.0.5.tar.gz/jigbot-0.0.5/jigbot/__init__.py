import os
import nltk
import string
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


class jigbot():
        def __init__(self, txt_file, name="Jiganesh"):
                self.name = name
                self.botspeech = name + ":  "
                self.txt_file = txt_file

                f = open(self.txt_file, 'r', errors='ignore')
                raw = f.read()
                nltk.download('punkt')
                nltk.download('wordnet')
                nltk.download('stopwords')
                sent_tokens = nltk.sent_tokenize(raw)
                word_tokens = nltk.word_tokenize(raw)

        def get_data(self):
                print(self.botspeech, "Please Fill your details for better Reach  !")
                bname, bemail, bnumber = True, True, True

                while bname:
                        print(self.botspeech, "Name format:  Input Name Middle name Surname")
                        name_of_person = input("User:  ")  # name_recorded
                        if len(name_of_person.split(" ")) >= 3:
                                bname = False

                while bemail:
                        print(self.botspeech, "Enter your email address")
                        address = input("User:  ")  # email is recorded
                        check = validate_email(address)
                        if check == True:
                                bemail = False

                while bnumber:
                        print(self.botspeech, "Enter your 10- digit Contact Number")
                        contact = input("User:  ")  # contact recorded
                        if len(contact) >= 10 and len(contact) <= 13 and contact.isdigit() == True:
                                bnumber = False
                print(self.botspeech, "Thank You")