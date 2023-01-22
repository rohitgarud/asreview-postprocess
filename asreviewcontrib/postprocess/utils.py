import re

def pre_process(text):
    # remove punctuations and digits 
    text = re.sub("[^a-zA-Z]", " ", text)
    return text