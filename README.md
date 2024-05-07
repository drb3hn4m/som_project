# Kohonen Challenge

### Notebook
The kohonen notebook includes the implementation by calling the classes from the modules dir.

### python main function
you can run the training via the main app along the required arguments:

```
python som_main.py \
--data_path=sample_data/colors_10.json \
--config_path=configs/config_40.yml \
--output_dir=output \
--output_format=png
```
----------------------------------
### Building a server by Fastapi
A Dockerfile is included to build a REST api server using fastapi for SOM project. You can buld and deploy it locally by following instructions:
```
git clone https://github.com/drb3hn4m/som_project.git
```


Build the server: 

```
cd som_project
docker build -t som_app .
docker run --rm --name som_server -p 8080:8080 som_app
```

to make a client request, open another terminal window if you are deploying it locally:
```
cd path/to/som_project
```

and then via you terminal to the "trainsom" endpoint

```
curl -X 'POST'   'http://localhost:8080/trainsom'   -H 'accept: application/json'   -H 'Content-Type: multipart/form-data'   -F 'input_json=@sample_data/colors_10.json;type=application/json'   -F 'config=@configs/config_40.yml;type=application/x-yaml'   -F 'format=png' --output W40.png
````
alternatively you can use the web user interface using the following link:

http://localhost:8080/docs

### Deployed server onto GCP
------------------------------------
Also the app is deloyed onto a VM on GCP you can access it via:
http://34.41.35.231:8080/docs

clearly you can also do a 
```
curl -X 'POST'  ....
```
 by replacing the localhosl in the above command with the above with external IP address

### Local dev/test docker
--------------------------
 for development purposes you can create a container from an image created by:

 ```
 docker build -f Dockerfile.dev -t som_app:dev .
 sudo docker run --rm --name som_container -d -i -t som_app:dev bash
 ```

 then bash into the container and run the app:
```
 docker exec -it som_container sh
```

 or alternatively you can attach to the container from vscode container extension (if enabled)
