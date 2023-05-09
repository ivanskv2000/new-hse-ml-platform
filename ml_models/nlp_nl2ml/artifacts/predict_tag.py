import os
import pickle
import cloudpickle
import pandas as pd
from sklearn.pipeline import make_pipeline
from lime.lime_text import LimeTextExplainer


def load_data(DATASET_PATH, sep=","):
    df = pd.read_csv(DATASET_PATH, encoding="utf-8", comment="#", sep=sep)
    df.dropna(axis=0, inplace=True)
    return df


def tfidf_transform(corpus, TFIDF_DIR):
    tfidf = cloudpickle.load(open(TFIDF_DIR, "rb"))
    features = tfidf.transform(corpus)
    return features


def inference(X, TAGS_TO_PREDICT, MODEL_DIR):
    clf = pickle.load(open(MODEL_DIR, "rb"))
    y_pred = clf.predict(X)
    return X, y_pred


def predict_tag(data_input_path, data_output_path, path_to_model_dir):
    GRAPH_VER = 5
    DATASET_PATH = os.path.join(data_input_path, "input.csv")
    MODEL = "svm"
    # svm or logreg

    TAGS_TO_PREDICT = [
        "import",
        "data_import",
        "data_export",
        "preprocessing",
        "visualization",
        "model",
        "deep_learning_model",
        "train",
        "predict",
    ]

    MODEL_DIR = os.path.join(
        path_to_model_dir,
        "artifacts/models/{}_regex_graph_v{}.sav".format(MODEL, GRAPH_VER),
    )
    TFIDF_DIR = os.path.join(
        path_to_model_dir,
        "artifacts/models/tfidf_{}_graph_v{}.pickle".format(MODEL, GRAPH_VER),
    )
    CODE_COLUMN = "code_block"

    df = load_data(DATASET_PATH)
    code_blocks = df[CODE_COLUMN]

    code_blocks_tfidf = tfidf_transform(code_blocks, TFIDF_DIR)
    _, y_pred = inference(code_blocks_tfidf, TAGS_TO_PREDICT, MODEL_DIR)

    df[TAGS_TO_PREDICT] = y_pred
    output_file_name = os.path.join(data_output_path, "output.csv")
    df.to_csv(output_file_name, index=False)


def explain_lime(data_input_path, explanation_output_path, path_to_model_dir, idx=None):
    GRAPH_VER = 5
    DATASET_PATH = os.path.join(data_input_path, "input.csv")
    MODEL = "svm"

    if not idx:
        idx = 0

    TAGS_TO_PREDICT = [
        "import",
        "data_import",
        "data_export",
        "preprocessing",
        "visualization",
        "model",
        "deep_learning_model",
        "train",
        "predict",
    ]

    MODEL_DIR = os.path.join(
        path_to_model_dir,
        "artifacts/models/{}_regex_graph_v{}.sav".format(MODEL, GRAPH_VER),
    )
    TFIDF_DIR = os.path.join(
        path_to_model_dir,
        "artifacts/models/tfidf_{}_graph_v{}.pickle".format(MODEL, GRAPH_VER),
    )

    if not os.path.exists(explanation_output_path):
        os.makedirs(explanation_output_path)

    CODE_COLUMN = "code_block"

    df = load_data(DATASET_PATH)
    code_blocks = df[CODE_COLUMN]

    tfidf = cloudpickle.load(open(TFIDF_DIR, "rb"))
    clf = pickle.load(open(MODEL_DIR, "rb"))

    estimators = clf.estimators_

    for i, estimator in enumerate(estimators):
        tag = TAGS_TO_PREDICT[i]
        class_names = ['None', tag]
        c = make_pipeline(tfidf, estimator)
        explainer = LimeTextExplainer(class_names=class_names)
        exp = explainer.explain_instance(code_blocks[idx], c.predict_proba, num_features=5)
        exp.save_to_file(os.path.join(explanation_output_path, 'explanation.html'), text=True)

        break
