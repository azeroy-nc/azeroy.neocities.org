# coding: utf-8
import json
import yaml

def load_data_from_file(item_type, path):
    from .data import dict_to_item_list
    with open(path, 'r') as file:
        if path.endswith('.json'):
            data_raw = json.load(file)
        elif path.endswith('.yml'):
            data_raw = yaml.safe_load(file)

        return dict_to_item_list(item_type, data_raw)
