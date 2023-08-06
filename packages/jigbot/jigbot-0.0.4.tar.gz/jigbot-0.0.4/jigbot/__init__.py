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


def get_data():
        print(botspeech, "Please Fill your details for better Reach  !")  # name_of_person is recorded
        name, email, number = True, True, True
        while name:
                print(botspeech, "Name format:  Input Name Middle name Surname")
                name_of_person = input("User:  ")
                if len(name_of_person.split(" ")) >= 3:
                        name = False

        while email:
                print(botspeech, "Enter your email address")
                address = input("User:  ")  # email is recorded
                check = validate_email(address)
                if check == True:
                        email = False

        while number:
                print(botspeech, "Enter your 10- digit Contact Number")
                contact = input("User:  ")  # contact recorded
                if len(contact) >= 10:
                        number = False
                print("Thank You")
