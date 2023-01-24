import re

with open("stopwords-en.txt", encoding="utf-8") as sw:
    STOPWORDS_EN = sw.readlines()
    STOPWORDS_EN = [word.replace("\n", "") for word in STOPWORDS_EN]


def pre_process(text):
    text = text.lower()
    text = text.split()
    # removing stopwords before removing punctuations because
    # stopwords include many words with apostrophe
    cleaned_text = [word for word in text if word not in STOPWORDS_EN]
    text = " ".join(cleaned_text)
    # remove punctuations and digits
    text = re.sub("[^a-zA-Z]", " ", text)
    text = re.sub(" +", " ", text)
    return text
