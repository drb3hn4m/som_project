# Deploying Kohonen Self Organizing Map (SOM)

The Kohonen Self Organizing Map (SOM) provides a data visualization technique which helps to understand high dimensional data by reducing the dimensions of data to a map. SOM also represents clustering concept by grouping similar data together.

Unlike other learning technique in neural networks, training a SOM requires no target vector. A SOM learns to classify the training data without any external supervision.

![Network](./assets/kohonen1.gif)

### Structure
A network has a width and a height that descibes the grid of nodes.  For example, the grid may be 4x4, and so there would be 16 nodes.

Each node has a weight for each value in the input vector.  A weight is simply a float value that the node multiplies the input value by to determine how influential it is (see below)

Each node has a set of weights that match the size of the input vector.  For example, if the input vector has 10 elements, each node would have 10 weights.


### Notebook
The kohonen notebook includes the details of the SOM algorithm along with the implementation by calling the classes from the modules dir.

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

------------------

### Deploying locally by kubenetes with minikube 
note that load balancer is available only on cloud so you need to create a nodeport service. Secondly the workaround to access the node (ip) is through mikikube tunnel service:
cd to the project dir, then:
```
kubectl apply -f som-server-local/configmap.yaml 
kubectl apply -f som-server-local/deployment.yaml
kubectl get pods
kubectl apply -f som-server-local/np_service.yaml
kubectl get service
minikube service som-trainer-np-service --url
```
it creates a tunnel then then use the printed IP and port to access and curl to the server. so you need to go the the root dir of repo and curl to the server given the minikube service IP an port:
```
curl -X 'POST'   'http://127.0.0.1:?????/trainsom'   -H 'accept: application/json'   -H 'Content-Type: multipart/form-data'   -F 'input_json=@sample_data/colors_10.json;type=application/json'   -F 'config=@configs/config_40.yml;type=application/x-yaml'   -F 'format=png' --output W40.png
```
---------------------
### Deploying on GCP by kubernetes
first build the image and store it on Artifact Registry:
```
gcloud builds submit --config=cloudbuild.yaml   --substitutions=_LOCATION="us-central1",_REPOSITORY="somapp",_IMAGE="somserver" .
```
setup kubernetes cluster:
```
gcloud config set compute/zone us-central1-a
PROJECT_ID=$(gcloud config get-value project)
CLUSTER_NAME=som-cluster
gcloud beta container clusters create $CLUSTER_NAME   --cluster-version=latest   --machine-type=e2-standard-4   --enable-autoscaling   --min-nodes=1   --max-nodes=3   --num-nodes=1 
gcloud container clusters get-credentials $CLUSTER_NAME 
````
apply the k8s manifests:
```
kubectl apply -f som-k8s-gcp/configmap.yaml 
kubectl apply -f som-k8s-gcp/deployment.yaml 
kubectl apply -f som-k8s-gcp/service.yaml 
kubectl get svc
```
use the printed external IP to curl to the endpoint:
```
curl -X 'POST'   'http://35.232.199.151:8080/trainsom'   -H 'accept: application/json'   -H 'Content-Type: multipart/form-data'   -F 'input_json=@sample_data/colors_10.json;type=application/json'   -F 'config=@configs/config_40.yml;type=application/x-yaml'   -F 'format=png' --output W40.png
```
note some of types above are redundant and can be shortened to:
```
curl -X 'POST'   'http://35.232.199.151:8080/trainsom'   -F 'input_json=@sample_data/colors_10.json'   -F 'config=@configs/config_40.yml'   -F 'format=png' --output W40_cl.png
```


to login into the github and configure it in gcp shell:

```
gh auth login
git config --global user.email "????@gmail.com"
git config --global user.name "???"
  ```
---------------------------
gcloud projects add-iam-policy-binding $GKE_PROJECT --member=serviceAccount:$SA_EMAIL --role=roles/container.admin
gcloud projects add-iam-policy-binding $GKE_PROJECT --member=serviceAccount:$SA_EMAIL --role=roles/storage.admin
gcloud projects add-iam-policy-binding $GKE_PROJECT --member=serviceAccount:$SA_EMAIL --role=roles/container.clusterViewer
gcloud artifacts repositories add-iam-policy-binding som-repo --location australia-southeast1 --member=serviceAccount:$SA_EMAIL --role=roles/artifactregistry.repoAdmin
gcloud iam service-accounts keys create key.json --iam-account=$SA_EMAIL

delete the resources by:
kubectl delete deployment --all --namespace=default


note that Github actions have a security feature that replaces strings that are also used as a secret. So if some log output just by accident contains the same string as used as a secret elsewhere it does get replaced with ***.

to print out the deployment pod manifest use:
kubectl get pods {pod name} -o yaml