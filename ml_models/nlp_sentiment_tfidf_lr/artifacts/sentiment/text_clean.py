import pymorphy2
import pandas as pd
from nltk.tokenize import word_tokenize

# строки download должны быть запущены, когда среда запускается в первый раз
# import nltk
# nltk.download('stopwords')
# nltk.download('punkt')

# try:
#     nltk.data.find('tokenizers/punkt')
# except LookupError:
#     nltk.download('punkt')

# try:
#     nltk.data.find('corpora/stopwords')
# except LookupError:
#     nltk.download('stopwords')

# Проблема с импортом - https://stackoverflow.com/questions/23704510/

from nltk.corpus import stopwords

ru_stops = set(stopwords.words("russian"))

# Подгружаем список всех полученных текстовых данных

ticker_list2 = [
    "ALRS",
    "CHMF",
    "GAZP",
    "GMKN",
    "LKOH",
    "MGNT",
    "MTSS",
    "NLMK",
    "NVTK",
    "ROSN",
    "SBER",
    "SNGS",
    "TATN",
    "YNDX",
    "AFKS",
    "AFLT",
    "AKRN",
    "AMEZ",
    "APTK",
    "AQUA",
    "BSPB",
    "CBOM",
    "CHMK",
    "DSKY",
    "DVEC",
    "ENRU",
    "FEES",
    "FESH",
    "GTRK",
    "HYDR",
    "IRAO",
    "IRGZ",
    "LNZL",
    "LSRG",
    "MAGN",
    "MOEX",
    "MRKC",
    "MRKP",
    "MRKU",
    "MRKV",
    "MRKY",
    "MRKZ",
    "MSNG",
    "MSRS",
    "MTLR",
    "MVID",
    "NKHP",
    "NMTP",
    "OGKB",
    "PHOR",
    "PIKK",
    "PLZL",
    "POLY",
    "RASP",
    "RNFT",
    "RSTI",
    "RTKM",
    "RUAL",
    "SELG",
    "SVAV",
    "TGKA",
    "TGKB",
    "TGKD",
    "TRMK",
    "TTLK",
    "UWGN",
    "VSMO",
    "VTBR",
    "MSST",
    "RKKE",
    "NKNC",
]

ticker_list = ["RKKE", "RNFT"]


def clean_and_combine(ticker_list):

    general_table = pd.DataFrame()

    # Очищаем весь текст от лишних знаков препинания и т.п.

    for k in ticker_list:

        text1 = pd.read_excel(str(k) + "_MFD.xlsx")
        text1_test = text1["posts"].astype(str)

        # text1_without = text1_test.str.replace("[\([{})\]]", "")
        # text1_without = text1_test.str.replace('[\n/!@#$%^&*()"№;—:?=|«»,.]', " ")
        # text1_without = text1_test.str.replace("[0-9+]", " ")
        text1_without = text1_test.str.replace("[^а-яА-Я]+", " ")

        def preprocess_text(text):
            # понижаем регистр у слов
            lower_text = text.lower()

            # токенизируем все слова в один лист
            tokens = word_tokenize(lower_text)

            return tokens

        # формируем готовых список токенизированных слов
        tokenized_final = []

        # проводим итерацию по всему списку
        for x in text1_without:

            token = preprocess_text(x)

            tokenized_final.append(token)

        morph = pymorphy2.MorphAnalyzer()

        def lemmatize(text):
            # words = text.split() # разбиваем текст на слова
            res = list()
            for word in text:
                p = morph.parse(word)[0]
                res.append(p.normal_form)

            return res

        # Лемматизируем все слова в нашей текстовой базе
        lemmatized_final = []

        # проводим итерацию по лемматизации слов
        for z in tokenized_final:

            lemma = lemmatize(z)

            lemmatized_final.append(lemma)

        # формируем списки очищенных и привеленных к начальной форме слов,
        # определяем каждый блок текстовых данных к своему тикеру
        clean_text = []
        for m in lemmatized_final:
            stop_m = [
                i for i in m if lemmatized_final not in stopwords.words("russian")
            ]
            clean_text.append(stop_m)
        clean_text

        ready_text = []
        for u in clean_text:
            row = " ".join(u)
            ready_text.append(row)

        ready_text1 = pd.DataFrame(ready_text)
        ready_text1.columns = ["cleaned_posts"]

        data = [text1["Date"], ready_text1["cleaned_posts"]]
        headers = ["Date", "cleaned_posts"]
        df3 = pd.concat(data, axis=1, keys=headers)
        name = k
        df3["ticker"] = str(name)

        general_table = general_table.append((df3))
    # сохраняем готовые данные
    return general_table
    # general_table.to_excel('cleaned_rusbaza.xlsx')


def clean_text_column(text_column):

    # text1_without = text1_test.str.replace("[\([{})\]]", "")
    # text1_without = text1_test.str.replace('[\n/!@#$%^&*()"№;—:?=|«»,.]', " ")
    # text1_without = text1_test.str.replace("[0-9+]", " ")
    text1_without = text_column.str.replace("[^а-яА-Я]+", " ")

    def preprocess_text(text):
        # понижаем регистр у слов
        lower_text = text.lower()

        # токенизируем все слова в один лист
        tokens = word_tokenize(lower_text)

        return tokens

    # формируем готовых список токенизированных слов
    tokenized_final = []

    # проводим итерацию по всему списку
    for x in text1_without:
        token = preprocess_text(x)
        tokenized_final.append(token)

    morph = pymorphy2.MorphAnalyzer()

    def lemmatize(text):
        # words = text.split() # разбиваем текст на слова
        res = list()
        for word in text:
            p = morph.parse(word)[0]
            res.append(p.normal_form)

        return res

    # Лемматизируем все слова в нашей текстовой базе
    lemmatized_final = []

    # проводим итерацию по лемматизации слов
    for z in tokenized_final:
        lemma = lemmatize(z)
        lemmatized_final.append(lemma)

    # формируем списки очищенных и привеленных к начальной форме слов,
    # определяем каждый блок текстовых данных к своему тикеру
    clean_text = []
    for m in lemmatized_final:
        stop_m = [i for i in m if lemmatized_final not in stopwords.words("russian")]
        clean_text.append(stop_m)

    ready_text = []
    for u in clean_text:
        row = " ".join(u)
        ready_text.append(row)

    ready_text1 = pd.DataFrame(ready_text)
    return ready_text1


def clean_data_frame(data_table):

    # Очищаем весь текст от лишних знаков препинания и т.п.

    text_column = data_table["posts"].astype(str)
    cleaned_text = clean_text_column(text_column)

    # cleaned_text.columns = ["cleaned_posts"]

    df3 = data_table.copy()

    df3.rename(columns={"posts": "cleaned_posts"}, inplace=True)
    df3["cleaned_posts"] = cleaned_text

    # data = [text1["Date"], cleaned_text["cleaned_posts"], text1["ticker"]]
    # headers = ["Date", "cleaned_posts", "ticker"]
    # df3 = pd.concat(data, axis=1, keys=headers)

    return df3
