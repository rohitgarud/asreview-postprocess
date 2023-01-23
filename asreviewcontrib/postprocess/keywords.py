import pandas as pd
import numpy as np
import re
import shutil
from pathlib import Path

from asreview import open_state
from asreview import ASReviewProject
from asreview import ASReviewData

from sklearn.feature_extraction.text import TfidfVectorizer
from fuzzywuzzy import process
from asreviewcontrib.postprocess.utils import pre_process


def extract_keywords(asreview_filename, outputfile_name, method, use_all_records=False):
    project_path = Path("tmp_data")
    try:
        shutil.rmtree(project_path)
    except:
        pass

    project_path.mkdir(parents=True, exist_ok=True)
    project = ASReviewProject.load(asreview_filename, project_path)

    dataset_fp = Path(
        project_path, project.config["id"], "data", project.config["dataset_path"]
    )
    dataset = ASReviewData.from_file(dataset_fp)

    with open_state(asreview_filename) as state:
        state_df = state.get_dataset()
        state_df["labeling_order"] = state_df.index
        state_df.rename(columns={"label": "current_label"}, inplace=True)

    dataset_w_labels = dataset.df.join(
        state_df.set_index("record_id")[["current_label"]], on="record_id"
    )

    # combine title and abstract into text
    dataset_w_labels["text"] = dataset.title + " " + dataset.abstract
    if use_all_records:
        dataset_included = dataset_w_labels.copy()
    else:
        dataset_included = dataset_w_labels[
            dataset_w_labels["current_label"] == 1
        ].copy()

    # Applying preprocessing to the dataset
    dataset_included["text"] = dataset_included["text"].apply(pre_process)

    corpus = dataset_included["text"].values

    dataset_included.drop(["current_label", "text"], axis=1, inplace=True)

    if method == "tf-idf":
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
            deduplicated_doc_keywords = list(process.dedupe(doc_keywords, threshold=70))
            final_keywords = ", ".join(deduplicated_doc_keywords)
            extracted_keywords.append(final_keywords)

        dataset_included = dataset_included.assign(
            extracted_keywords=extracted_keywords
        )

    else:
        raise ValueError(
            "This keyword extraction method is not implemented. Please select 'tf-idf'."
        )

    dataset_included.to_csv(outputfile_name)
    shutil.rmtree(project_path)
