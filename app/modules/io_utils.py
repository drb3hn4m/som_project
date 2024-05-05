import json
import numpy as np
import yaml
from collections import namedtuple
from PIL import Image
import copy
import os 

def json_loader(file_path):
    with open(file_path, 'r') as json_file:
        json_data = json.load(json_file)
    input_data = np.array(json_data)
    return input_data

def dict_to_namedtuple(dictionary):
    for key, value in dictionary.items():
        if isinstance(value, dict):
            dictionary[key] = dict_to_namedtuple(value)
    return namedtuple(key.capitalize(), dictionary.keys())(**dictionary)

def config_loader(filename):
    with open(filename, 'r') as config_file:
        config_dict = yaml.safe_load(config_file)
    return dict_to_namedtuple(config_dict)

def json_writer(data,file_path):
    dir = "/".join(file_path.split("/")[0:-1])
    if not os.path.exists(dir):
        os.makedirs(dir)    
    array_list = data.tolist()
    json_data = json.dumps(array_list)
    with open(file_path, 'w') as json_file:
        json_file.write(json_data)

def image_writer(inp_arr,file_path):
    dir = "/".join(file_path.split("/")[0:-1])
    if not os.path.exists(dir):
        os.makedirs(dir)    
    arr=copy.deepcopy(inp_arr)*255
    arr = arr.astype(np.int8)
    img = Image.fromarray(arr ,mode='RGB')
    img.save(file_path)