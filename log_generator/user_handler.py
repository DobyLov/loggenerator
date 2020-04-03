""" user handler """

import uuid, random
from random import choice as randchoice
from .words_constants import ADJECTIVES, NOUNS

# Génère un pseudo nom avec @ en préfixe et avec ou sans underscore
def get_name():
    adjective = randchoice(ADJECTIVES)
    noun = randchoice(NOUNS)
    camel_case_adjective = " @" + adjective[0].upper() + adjective[1:]
    camel_case_noun = noun[0].upper() + noun[1:]
    underscores = randomUnderscore()
    if underscores:
        name: str = camel_case_adjective + camel_case_noun
    else:
        name: str = camel_case_adjective + "_" + camel_case_noun
    return name

# Random pour mettre un underscore dans le Tweeter username
def randomUnderscore():
    return random.choice([True, False])

# Age aléatoire entre 18 et 99 
def get_age():
    age = random.randint(18,99)
    return age

# UuidGen
def get_uuid():
    return str(uuid.uuid4())