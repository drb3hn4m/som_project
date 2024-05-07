## Kohonen Challenge

Building a REST api for SOM prject: 
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

and then via you terminal

```
curl -X 'POST'   'http://localhost:8080/trainsom'   -H 'accept: application/json'   -H 'Content-Type: multipart/form-data'   -F 'input_json=@sample_data/colors_10.json;type=application/json'   -F 'config=@configs/config_40.yml;type=application/x-yaml'   -F 'format=png' --output W40.png
````
alternatively you can use the web user interface using the following link:

http://localhost:8080/docs


Also the app is deloyed onto a VM on GCP you can access it via:
http://34.41.35.231:8080/docs

clearly you can do a 
```
curl -X 'POST'  ....
```
 by replacing the localhosl in the above command with the above with external IP address