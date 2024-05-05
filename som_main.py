from modules.SelfOrganizingMap import SelfOrganizingMap as som
from modules.io_utils import *
import argparse


def main(input_data,hyper_params):
    som_obj = som(NetworkShape = hyper_params.som.NetworkShape,MaxIter=hyper_params.som.MaxIter,alpha = hyper_params.som.alpha)
    W = som_obj.train(input_data)
    return W

if __name__=="__main__":
    parser = argparse.ArgumentParser(description="Algorithm for traning a Self Organazing Map")
    parser.add_argument("--config_path", type=str, default= "configs/config_base.yml", help="config path for som")
    parser.add_argument("--data_path", type=str, default= "sample_data/colors_10.json", help="input data path to som")
    parser.add_argument("--output_dir", type=str, default= "output", help="directory of output")
    parser.add_argument("--output_format", type=str, default= "json", choices = ["png","json"],help="output formats")
    args = parser.parse_args()
    input_data = json_loader(args.data_path)
    hyper_params = config_loader(args.config_path)
    output_data = main(input_data,hyper_params)
    output_path = args.output_dir+"/result_"+args.data_path.split("/")[-1].split(".")[-2]+ f"_grid_{hyper_params.som.NetworkShape[0]}by{hyper_params.som.NetworkShape[1]}"  +"."+args.output_format
    if args.output_format == "json":
        json_writer(output_data,output_path)
    elif args.output_format == "png":
        image_writer(output_data,output_path)