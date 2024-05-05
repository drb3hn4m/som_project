import json
import numpy as np
import yaml
from collections import namedtuple
from PIL import Image
import copy
import os 
from fastapi.responses import StreamingResponse

def dict_to_namedtuple(dictionary):
    for key, value in dictionary.items():
        if isinstance(value, dict):
            dictionary[key] = dict_to_namedtuple(value)
    return namedtuple(key.capitalize(), dictionary.keys())(**dictionary)

async def load_server_args(input_req,config):
    input_str = json.load(input_req.file)
    input_data =  np.array(input_str)

    config_contents = await config.read()
    config_data = yaml.safe_load(config_contents)
    hyper_params = dict_to_namedtuple(config_data)
    return input_data,hyper_params

def respond_in_json(W):
    print("writing json response ...")
    W_json = json.dumps(W.tolist())
    async def generate():
        # Yield the JSON data
        yield W_json.encode()
    return StreamingResponse(generate(),media_type="application/json")

def respond_in_png(W):
    print("writing png response ...")
    arr=copy.deepcopy(W)*255
    arr = arr.astype(np.int8)
    img = Image.fromarray(arr ,mode='RGB')
    img = Image.fromarray(arr ,mode='RGB')
    img.save('tmp.png')
    file_image = open(f'tmp.png', mode="rb")
    return StreamingResponse(file_image, media_type="image/jpeg")