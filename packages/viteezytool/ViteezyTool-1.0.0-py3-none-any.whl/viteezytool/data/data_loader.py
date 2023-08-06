from tkinter import Tk
from tkinter.filedialog import askopenfilename, askdirectory
from pathlib import Path
import pandas as pd
import yaml
import sys
import json

from viteezytool.data.shared import cfg

Tk().withdraw()


def save_folder():
    folder = askdirectory(title="Selecteer een output folder")
    if len(folder) > 1:
        return Path(folder)
    else:
        return cfg.OUTPUT


def load_excel(sheet_name: str = None):
    try:
        openpath = askopenfilename(title='Selecteer excel bestand')
    except AttributeError:
        sys.exit()
    if len(openpath) > 1:
        data = pd.read_excel(openpath, sheet_name=sheet_name)
        if sheet_name == cfg.SHEET:
            data = data[data[cfg.C_KEY].notna()]
        return data
    else:
        return


def dict_clean(items):
    result = {}
    for key, value in items:
        if value is None:
            value = ' '
        result[key] = value
    return result


def load_pills():
    open_path = (cfg.RESOURCES / 'pills.yaml').absolute().as_posix()
    with open(open_path) as stream:
        try:
            pills = yaml.safe_load(stream)
            dict_str = json.dumps(pills)
            pills = json.loads(dict_str, object_pairs_hook=dict_clean)
            return pills
        except yaml.YAMLError as exc:
            print(exc)


def load_lookup():
    open_path = (cfg.RESOURCES / 'lookup.xlsx').absolute().as_posix()
    return pd.read_excel(open_path, sheet_name='Sheet1')


def lookup_by_id(id, table: pd.DataFrame):
    item = table.loc[table.id == id]
    return item.to_numpy()[0]


if __name__ == '__main__':
    df = load_excel()
