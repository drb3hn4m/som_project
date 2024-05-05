## Kohonen Challenge

Please see [kohonen.ipynb](kohonen.ipynb)

how to build the server: 
docker build -t som_app .

docker run --rm --name som_server -p 8080:8080 som_app

how to make a client request:
curl -X 'POST'   'http://localhost:8080/trainsom'   -H 'accept: application/json'   -H 'Content-Type: multipart/form-data'   -F 'input_json=@sample_data/colors_10.json;type=application/json'   -F 'config=@configs/config_40.yml;type=application/x-yaml'   -F 'format=png' --output W40.png
