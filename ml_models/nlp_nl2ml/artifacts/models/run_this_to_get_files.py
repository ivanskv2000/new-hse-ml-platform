import requests
import shutil


def get_file_yadisk(url, local_filename):

    headers = {"Accept": "application/json", "Content-Type": "application/json"}

    r = requests.get(
        "https://cloud-api.yandex.net/v1/disk/public/resources/download",
        params={"public_key": url},
    )
    print(r)
    response_json = r.json()
    direct_link = response_json["href"]

    with requests.get(direct_link, stream=True) as r:
        with open(local_filename, "wb") as f:
            shutil.copyfileobj(r.raw, f)


get_file_yadisk("https://disk.yandex.ru/d/bxyQ01hlr3DjUA", "svm_regex_graph_v5.sav")
get_file_yadisk("https://disk.yandex.ru/d/_fz49NbTnIy7nw", "tfidf_svm_graph_v5.pickle")
