# Sentiment classification

## Установка

```sh
python -m pip install -r requirements.txt
```

Больше ничего не должно быть нужно.

## Запуск

```sh
python exec_script.py -p full_path_to_parameters.json
```

## Параметры `.json`

**path_to_model_dir** - полный путь к папке модели (внутри которой artifacts, exec_script, и т.д.)

**data_input_path** - полный путь к файлу с входными данными. Пример в `data/run_id_1sentiment1234/input/input.csv`.

**data_output_path** - полный путь к папке, куда нужно писать выходные данные.

### model_parameters

**model_type** - строка. Сейчас единственное возможное значение - `logreg`.

**vec_type** - строка. Сейчас  единственное возможное значение - `tfidf`.

Оба необязательны.
