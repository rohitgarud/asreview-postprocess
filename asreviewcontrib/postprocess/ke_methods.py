import numpy as np
import string

from fuzzywuzzy import process
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer

from asreviewcontrib.postprocess.utils import pre_process


def ke_tfidf(corpus):

    corpus = [pre_process(text) for text in corpus]
    # Initialising TF-IDF vectorizer
    vectorizer = TfidfVectorizer(
        stop_words="english", max_df=0.8, ngram_range=(1, 3), max_features=10000
    )
    # Fit and transform the text
    tfidf = vectorizer.fit_transform(corpus)

    # Get the feature names
    feature_names = vectorizer.get_feature_names_out()

    # Get top 10 keywords for the document and reduce duplication
    extracted_keywords = []
    for doc_tfidf in tfidf.toarray():
        sorted_ids_top10 = np.argsort(doc_tfidf)[-10:][::-1]
        doc_keywords = feature_names[sorted_ids_top10].tolist()
        # Reducing duplication in keywords
        deduplicated_doc_keywords = list(process.dedupe(doc_keywords, threshold=70))
        final_keywords = ", ".join(deduplicated_doc_keywords)
        extracted_keywords.append(final_keywords)
    return extracted_keywords


def ke_rake(corpus):
    try:
        from rake_nltk import Rake
    except ModuleNotFoundError:
        print(
            "The RAKE keyword extraction method requires the rake-nltk package to be installed. Use pip install rake-nltk or install optional ASReview-Postprocess dependencies for RAKE with pip install asreview-postprocess[rake] or install all optional ASReview-Postprocess dependencies with pip install asreview-postprocess[all]"
        )

    extracted_keywords = []
    # list of punctuations used as delimiters in RAKE algorithm for splitting text
    punctuations = [punc for punc in string.punctuation]
    punctuations.extend(["*.", "--", ").", "),", "?,"])

    for text in corpus:
        r = Rake(
            stopwords=set(stopwords.words("english")),
            punctuations=punctuations,
            include_repeated_phrases=False,
            min_length=1,
            max_length=3,
        )
        r.extract_keywords_from_text(text)
        doc_keywords = r.get_ranked_phrases()
        # Reducing duplication in keywords
        deduplicated_doc_keywords = list(process.dedupe(doc_keywords, threshold=70))
        final_keywords = ", ".join(deduplicated_doc_keywords[:5])
        extracted_keywords.append(final_keywords)
    return extracted_keywords


def ke_yake(corpus):
    try:
        import yake
    except ModuleNotFoundError:
        print(
            "The YAKE keyword extraction method requires the yake package to be installed. Install optional ASReview-Postprocess dependencies for YAKE with pip install asreview-postprocess[yake] or install all optional ASReview-Postprocess dependencies with pip install asreview-postprocess[all]"
        )

    extracted_keywords = []
    for text in corpus:
        y = yake.KeywordExtractor(
            n=3,  # maximum ngram size
            dedupLim=0.7,  # deduplication threshold
            dedupFunc="seqm",  # deduplication algorithm
            top=20,
            features=None,
        )
        doc_keywords = [keyword[0] for keyword in y.extract_keywords(text)]
        deduplicated_doc_keywords = list(process.dedupe(doc_keywords, threshold=70))
        final_keywords = ", ".join(deduplicated_doc_keywords[:5])
        extracted_keywords.append(final_keywords)
    return extracted_keywords


def ke_textrank(corpus):
    import subprocess

    try:
        import pytextrank
    except ModuleNotFoundError:
        print(
            "The TextRank keyword extraction method requires the 'pytextrank' package to be installed. Install optional ASReview-Postprocess dependencies for TextRank with pip install asreview-postprocess[textrank] or install all optional ASReview-Postprocess dependencies with pip install asreview-postprocess[all]"
        )

    import spacy

    subprocess.run(["spacy", "download", "en_core_web_sm"])

    corpus = [pre_process(text) for text in corpus]

    # load a spaCy model
    nlp = spacy.load("en_core_web_sm")
    stopwords = nlp.Defaults.stop_words
    # add PyTextRank to the spaCy pipeline
    nlp.add_pipe("textrank")

    extracted_keywords = []
    for text in corpus:
        doc = nlp(text)
        doc_keywords = [
            keyword.text for keyword in doc._.phrases if len(keyword.text.split()) <= 3
        ]
        deduplicated_doc_keywords = list(process.dedupe(doc_keywords, threshold=70))
        final_keywords = ", ".join(deduplicated_doc_keywords[:5])
        extracted_keywords.append(final_keywords)
    return extracted_keywords
