import argparse
from artifacts.sentiment.sentiment import run_inference_pipeline
import json


parser = argparse.ArgumentParser(description="Run pipeline for model Teplova_Sentiment")
parser.add_argument(
    "-p", "--params", type=str, help="path to request.json file with parameters"
)

args = parser.parse_args()
with open(args.params) as jf:
    params = json.load(jf)


model_types = [
    "logreg",
    # "naive_bayes",
]

vectorization_types = [
    "tfidf",
    # "bag_of_words",
]

path_to_model_dir = params["path_to_model_dir"]
data_input_path = params["data_input_path"]
data_output_path = params["data_output_path"]

model_type = params["model_parameters"].get("model_type", "logreg")
vec_type = params["model_parameters"].get("vec_type", "tfidf")

run_inference_pipeline(
    data_input_path, data_output_path, path_to_model_dir, model_type, vec_type
)
