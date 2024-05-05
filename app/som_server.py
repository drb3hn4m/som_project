
from typing import Union
from fastapi import FastAPI, File, UploadFile, Form
import json
import numpy as np 
from typing import Annotated
from modules.SelfOrganizingMap import SelfOrganizingMap as som
from modules.server_io_utils import *

app = FastAPI(title = 'Deploying the SOM model via FastAPI',debug=True)
@app.post("/trainsom")
async def train_som(input_json: Annotated[UploadFile, File()],
                    config: Annotated[UploadFile, File()],
                    format: Annotated[str, Form()]):
    # input_data,hyper_params = load_server_args(input_req,config)
    input_data =  np.array(json.load(input_json.file))
    config_data = yaml.safe_load(await config.read())
    hyper_params = dict_to_namedtuple(config_data)
    print("input arguments are loaded")
    som_network = som(NetworkShape = hyper_params.som.NetworkShape,MaxIter=hyper_params.som.MaxIter,alpha = hyper_params.som.alpha)
    W = som_network.train(input_data)
    if format == "json":
        return respond_in_json(W)
    if format == "png":
        return respond_in_png(W)

@app.get("/")
def hello_page():
    return "this is the main home page of the som app, to access the app go to http://120.0.0.1:8080/docs"