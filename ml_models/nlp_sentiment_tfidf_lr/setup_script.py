import subprocess
import sys
import os

path_to_reqs = os.path.join("ml_models", "nlp_sentiment_tfidf_lr", "requirements.txt")
subprocess.run(
    [
        sys.executable,
        "-m",
        "pip",
        "install",
        "-r",
        path_to_reqs,
    ]
)
