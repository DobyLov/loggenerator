""" HashTags handler """

import random
from random import choice as randchoice
from .words_constants import HASHTAGS

# Générer la string de 1 ou x Hashtag(s)
def gen_Hashtags():
    hashtagsArray = []
    nbHastag = randomNbHashtags()
    hashTagStr = randomHashtags()
    hashtagsArray.append(hashTagStr)
    for i in range(nbHastag):
        if i > 1:
            addAshtag = randomHashtags() 
            while checkHashTagIsPresent(hashtagsArray, addAshtag) == True:
                addAshtag = randomHashtags()
            addSeparator:str = ('"' + ", " + '"') 
            hashTagStr = hashTagStr + addSeparator + addAshtag
            hashtagsArray.append(addAshtag)

    return str('["' + hashTagStr + '"]'), hashtagsArray

# Random pour le nombre de #HASTAGS 1, 2, 3, 4, 5
def randomNbHashtags():
    return random.randrange(1, 10, 1)

# Random sur les Hashtags
def randomHashtags():
    return randchoice(HASHTAGS)

# Check if hashtag is already present in 
def checkHashTagIsPresent(givenHashTagsArray, givenHashTag:str):
    hTagIsPresent:bool = False
    for hTags in givenHashTagsArray:
        if hTags == givenHashTag:
            hTagIsPresent = True
            break
    return hTagIsPresent