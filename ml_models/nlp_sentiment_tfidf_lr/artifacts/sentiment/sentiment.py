import pandas as pd
from sklearn.linear_model import LogisticRegression
import pickle
from .text_clean import clean_data_frame
import os
from lime.lime_text import LimeTextExplainer
from sklearn.pipeline import make_pipeline

num_words = 100000
max_review_len = 5000


def fit_logreg(x_train, y_train):

    lr = LogisticRegression(
        class_weight="balanced",
        solver="liblinear",
        penalty="l2",
        random_state=42,
        max_iter=1000,
    )
    lr.fit(x_train, y_train)
    return lr


def tfidf_vectorize(data_table, path_to_checkpoints):
    posts = data_table["cleaned_posts"]

    count_vect = load_count_vect(path_to_checkpoints)
    x_counts = count_vect.transform(posts)
    tfidf_transformer = load_tfidf_transformer(path_to_checkpoints)
    x_tfidf = tfidf_transformer.transform(x_counts)

    return x_tfidf


def load_tfidf_transformer(path_to_checkpoints):
    load_path = os.path.join(path_to_checkpoints, "tfidf_transformer.pkl")
    with open(load_path, "rb") as f:
        tfidf_transformer = pickle.load(f)
    return tfidf_transformer


def load_count_vect(path_to_checkpoints):
    load_path = os.path.join(path_to_checkpoints, "count_vect.pkl")
    with open(load_path, "rb") as f:
        count_vect = pickle.load(f)
    return count_vect


def load_model(path):
    with open(path, "rb") as f:
        return pickle.load(f)


def run_inference_pipeline(
    data_input_path,
    data_output_path,
    path_to_model_dir,
    model_type="logreg",
    vec_type="tfidf",
):
    # Изначально данные "грязные"
    # Столбцы: datetime, text, ticker, sentiment (empty)
    dirty_data_table = pd.read_csv(os.path.join(data_input_path, "input.csv"))

    data_table = clean_data_frame(dirty_data_table)

    # model_dir = "ml_models/nlp/sentiment_bow_lr/artifacts/models/"

    model_filename = f"{model_type}_{vec_type}.pickle"
    path_to_checkpoints = os.path.join(path_to_model_dir, "artifacts", "models")
    path_to_model = os.path.join(path_to_checkpoints, model_filename)

    model = load_model(path_to_model)

    data_table = data_table.dropna()
    x_data = tfidf_vectorize(data_table, path_to_checkpoints)
    y_data = model.predict(x_data)
    y_series = pd.Series(y_data, name="Sentiment")

    # Возвращаются исходные "грязные" данные вместе с сентиментом
    data_columns = [dirty_data_table, y_series]
    output_table = pd.concat(data_columns, axis=1, ignore_index=True)

    output_file_name = "output.csv"
    output_file_path = os.path.join(data_output_path, output_file_name)

    output_table.to_csv(output_file_path)
    return output_table


def explain_lime(data_input_path, explanation_output_path, path_to_model_dir, idx=None):

    if not idx:
        idx = 0

    if not os.path.exists(explanation_output_path):
        os.makedirs(explanation_output_path)

    dirty_data_table = pd.read_csv(os.path.join(data_input_path, "input.csv"))
    data_table = clean_data_frame(dirty_data_table)

    model_type = "logreg"
    vec_type = "tfidf"
    model_filename = f"{model_type}_{vec_type}.pickle"
    path_to_checkpoints = os.path.join(path_to_model_dir, "artifacts", "models")
    path_to_model = os.path.join(path_to_checkpoints, model_filename)

    model = load_model(path_to_model)
    countvec = load_count_vect(path_to_checkpoints)
    transformer = load_tfidf_transformer(path_to_checkpoints)

    data_table = data_table.dropna()
    posts = data_table["cleaned_posts"]

    c = make_pipeline(countvec, transformer, model)
    explainer = LimeTextExplainer(class_names=None)
    exp = explainer.explain_instance(posts[idx], c.predict_proba, num_features=5)
    exp.save_to_file(
        os.path.join(explanation_output_path, "explanation.html"), text=True
    )
