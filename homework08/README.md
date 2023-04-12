# Human Genome API, now with Kubernetes!

This project creates a simple, containerized, Kubernetes-deployed Flask API to process HTTP requests for human genome data. [More details](https://www.genenames.org/download/archive/) and the [source data](https://ftp.ebi.ac.uk/pub/databases/genenames/hgnc/json/hgnc_complete_set.json) can be found via the HUGO Gene Nomenclature Committee website. The application pulls the data from the web and stores it in a Kubernetes/Docker-containerized Redis database for queries, which is periodically saved to a persistent volume claim via a volume mount. This means that application data persists even if the application is stopped or, in the worst case, crashes.

This assignment is important because it synthesizes several software engineering concepts. Extending beyond all of the value in the previous assignment, it uses Kubernetes to orchestrate the deployment of containers. Unlike before, there can be deployments of multiple copies of a container which tag-team to accommodate high request loads. If a container fails or is deleted, the deployment quickly replaces it with a new one, optionally with the most up-to-date image. Finally, the data itself is put into its own persistent volume claim to further containerize it.

## Running the Project

It is recommended to run the project from images pulled from [Docker Hub](https://hub.docker.com/repository/docker/ashtonvcole/genome_database/). The user is also welcome to build their own images. For alternative, non-Kubernetes methods, see [Homework 6](../homework06).

Regardless of how the images are obtained, they can be implemented with a single command.

```bash
kubectl apply \
-f gdb-rd-pvc.yml \
-f gdb-rd-deployment.yml \
-f gdb-rd-service.yml \
-f gdb-flask-deployment.yml \
-f gdb-flask-service.yml \
-f pythondebug-deployment.yml
```

This instructs Kubernetes to create the containers, services, and persistent volume claim for the Flask and Redis applicatons. More details on this are in [Project Structure](#project-structure).

As-is, the service IP addresses are not necessarily public. This means that you may not be able to access the API directly from your machine, even if you identify the service IP address. To test the API, you may enter a `pythondebug-deployment` pod. First find the name of the active pod.

```bash
kubectl get pods --selector=app=ashtonc-test-pythondebug-app
```

```
NAME                                                   READY   STATUS    RESTARTS   AGE
ashtonc-test-pythondebug-deployment-7c77fbc6b4-vb8tz   1/1     Running   0          6m11s
```

Enter this pod and run a bash shell.

```
kubectl exec -it ashtonc-test-pythondebug-deployment-7c77fbc6b4-vb8tz -- /bin/bash
```

From here, you can access the Flask service by curling to the Flask service's name, specified in its YAML file, through the standard port 5000.

```
curl 'http://ashtonc-test-gdb-flask-service:5000/data' -X GET
```

Note that to get a non-empty result from the above, you must call the appropriate endpoint and HTTP method.

To update either the Flask or Redis applications from a new image, simply delete the respective pods. Since the image pull policies are set to always, the new pods which are restarted will have the updates. For example, the following deletes the Flask pods.

```bash
kubectl delete pods --selector=app=ashtonc-test-gdb-flask-app
```

To stop the project, you must delete the services, deployments, and persistent volume claims.

```bash
kubectl delete deployment ashtonc-test-pythondebug-deployment; \
kubectl delete service ashtonc-test-gdb-flask-service; \
kubectl delete deployment ashtonc-test-gdb-flask-deployment; \
kubectl delete service ashtonc-test-gdb-rd-service; \
kubectl delete deployment ashtonc-test-gdb-rd-deployment; \
kubectl delete pvc ashtonc-test-gdb-rd-pvc
```

## Project Structure

- `Dockerfile` [About](#dockerfile) [File](Dockerfile)
- `genome_database.py` [About](#genome_databasepy) [File](genome_database.py)
- `gdb-rd-pvc.yml` [About](#gdb-rd-pvcyml) [File](gdb-rd-pvc.yml)
- `gdb-rd-deployment.yml` [About](#gdb-rd-deploymentyml) [File](gdb-rd-deployment.yml)
- `gdb-rd-service.yml` [About](#gdb-rd-serviceyml) [File](gdb-rd-service.yml)
- `gdb-flask-deployment.yml` [About](#gdb-flask-deploymentyml) [File](gdb-flask-deployment.yml)
- `gdb-flask-service.yml` [About](#gdb-flask-serviceyml) [File](gdb-flask-service.yml)
- `pythondebug-deployment.yml` [About](#gdb-flask-deploymentyml) [File](pythondebug-deployment.yml)

### `Dockerfile`

This script is used to build a Docker image, which can excecute the program within a container.

### `genome_database.py`

This script processes all HTTP requests to the API. In addition to code that initializes the server, it contains several functions which execute and return data for a certain endpoint.

### `gdb-rd-pvc.yml`

This defines the `ashtonc-test-gdb-rd-pvc` `PersistentVolumeClaim` object. It sets up a persistent volume claim which saves the data from the Redis application.

### `gdb-rd-deployment.yml`

This defines the `ashtonc-test-gdb-rd-deployment` `Deployment` object. It sets up a single pod which has a Docker container of Redis. This pod has the selector `app=ashtonc-test-gdb-rd-app`.

### `gdb-rd-service.yml`

This defines the `ashtonc-test-gdb-rd-service` `Service` object. It sets up a Cluster IP service with a fixed IP address which routes HTTP requests to the `ashtonc-test-gdb-rd-deployment` pod via port 6379. This service has an alias for its IP address `ashtonc-test-gdb-rd-service` and the selector `app=ashtonc-test-gdb-rd-app`.

### `gdb-flask-deployment.yml`

This defines the `ashtonc-test-gdb-flask-deployment` `Deployment` object. It sets up two pods which have Docker containers of the Python Flask application. This pod has the selector `app=ashtonc-test-gdb-flask-app`.

### `gdb-flask-service.yml`

This defines the `ashtonc-test-gdb-flask-service` `Service` object. It sets up a Cluster IP service with a fixed IP address which routes HTTP requests to `ashtonc-test-gdb-flask-deployment` pods via port 5000. This service has an alias for its IP address `ashtonc-test-gdb-flask-service` and the selector `app=ashtonc-test-gdb-flask-app`.

### `pythondebug-deployment.yml`

This defines the `ashtonc-test-pythondebug-deployment` `Deployment` object. It sets up a single pod which has a Docker container of Python 3.8.10. This pod has the selector `app=ashtonc-test-pythondebug-app`. This pod is not strictly necessary, but it is helpful for debugging, both with bash `curl`-based and Python-based HTTP requests.

## Endpoints

The following endpoints are available to the user. Note that all endpoints, given irregular inputs or error conditions, will return a string message with a 404 status code.

- [`/data`](#data)
- [`/genes`](#genes)
- [`/genes/hgnc_id`](#geneshgnc_id)

### `/data`

#### `POST`

This pulls the source data from online and adds it to the Redis database.

```bash
curl 'http://ashtonc-test-gdb-flask-service:5000/data' -X POST
```

```
Data successfully posted
```

#### `GET`

This retrieves all data from the Redis database and returns it in JSON form. Since the data set is large, it is not recommended to get the data directly, but to pipe it into a file.

```bash
curl 'http://ashtonc-test-gdb-flask-service:5000/data' -X GET > out.json
head out.json
```

```json
[
  {
    "_version_": "1761599381015887872",
    "agr": "HGNC:35163",
    "alias_name": "long intergenic non-protein coding RNA 978|adipogenesis down-regulated transcript 2|lncRNA associated with poor prognosis of HCC|myeloid RNA regulator of Bim-induced death",
    "alias_symbol": "LINC00978|AGD2|AK001796|lncRNA-AWPPH|MORRBID",
    "date_approved_reserved": "2013-07-01",
    "date_modified": "2017-06-15",
    "date_name_changed": "2015-04-22",
    "date_symbol_changed": "2015-04-22",
```

#### `DELETE`

This clears the Redis database.

```bash
curl 'http://ashtonc-test-gdb-flask-service:5000/data' -X DELETE
```

```
Data successfully deleted
```

### `/genes`

This returns a list of all of the `hgnc_id`'s for each entry in the data set, in JSON form. Since it is unique, this can be considered a primary key for the data set.

```bash
curl 'http://ashtonc-test-gdb-flask-service:5000/genes' -X GET > out.json
head out.json
```

```json
[
  "HGNC:35163",
  "HGNC:3867",
  "HGNC:38146",
  "HGNC:760",
  "HGNC:29947",
  "HGNC:26102",
  "HGNC:52109",
  "HGNC:1826",
  "HGNC:51704",
```

### `/genes/<hgnc_id>`

This returns the data for the entry specified by `hgnc_id` in JSON form. If the data set is empty, the gene doesn't exist, or the inputs are poorly formed, it will return a string message with a 404 status code.

```bash
curl 'http://ashtonc-test-gdb-flask-service:5000/genes/HGNC:35163' -X GET
```

```json
{
  "_version_": "1761599381015887872",
  "agr": "HGNC:35163",
  "alias_name": "long intergenic non-protein coding RNA 978|adipogenesis down-regulated transcript 2|lncRNA associated with poor prognosis of HCC|myeloid RNA regulator of Bim-induced death",
  "alias_symbol": "LINC00978|AGD2|AK001796|lncRNA-AWPPH|MORRBID",
  "date_approved_reserved": "2013-07-01",
  "date_modified": "2017-06-15",
  "date_name_changed": "2015-04-22",
  "date_symbol_changed": "2015-04-22",
  "ena": "BX647931",
  "ensembl_gene_id": "ENSG00000172965",
  "entrez_id": "541471",
  "gene_group": "MicroRNA non-coding host genes",
  "gene_group_id": "1688",
  "hgnc_id": "HGNC:35163",
  "lncipedia": "MIR4435-2HG",
  "location": "2q13",
  "location_sortable": "02q13",
  "locus_group": "non-coding RNA",
  "locus_type": "RNA, long non-coding",
  "mgd_id": "MGI:3652191",
  "name": "MIR4435-2 host gene",
  "omim_id": "617144",
  "prev_name": "MIR4435-1 host gene (non-protein coding)|MIR4435-1 host gene",
  "prev_symbol": "MIR4435-1HG",
  "pubmed_id": "19531736|25888808|27525555",
  "refseq_accession": "NR_015395",
  "rna_central_id": "URS0000A77756",
  "status": "Approved",
  "symbol": "MIR4435-2HG",
  "uuid": "24bb4cfb-01e7-4fdd-966b-3d5e1776d2c6",
  "vega_id": "OTTHUMG00000150313"
}
```
