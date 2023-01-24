import shutil
from pathlib import Path

from asreview import open_state
from asreview import ASReviewProject
from asreview import ASReviewData

from asreviewcontrib.postprocess.utils import pre_process
import asreviewcontrib.postprocess.ke_methods as ke


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

    if method == "tf-idf":
        # Applying preprocessing to the dataset
        dataset_included["text"] = dataset_included["text"].apply(pre_process)

    corpus = dataset_included["text"].values

    if method == "tf-idf":
        extracted_keywords = ke.ke_tfidf(corpus)

    elif method == "rake":
        extracted_keywords = ke.ke_rake(corpus)

    elif method == "yake":
        extracted_keywords = ke.ke_yake(corpus)

    else:
        raise ValueError(
            "This keyword extraction method is not implemented. Please select from [tf-idf, rake, yake]."
        )

    dataset_included = dataset_included.assign(extracted_keywords=extracted_keywords)
    dataset_included.drop(["current_label", "text"], axis=1, inplace=True)
    dataset_included.to_csv(outputfile_name)
    shutil.rmtree(project_path)
