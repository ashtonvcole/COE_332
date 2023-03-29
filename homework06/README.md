# Human Genome API

This project creates a simple, containerized, locally-hosted Flask API to process HTTP requests for human genome data. [More details](https://www.genenames.org/download/archive/) and the [source data](https://ftp.ebi.ac.uk/pub/databases/genenames/hgnc/json/hgnc_complete_set.json) can be found via the HUGO Gene Nomenclature Committee website. The application pulls the data from the web and stores it in a Docker-containerized Redis database for queries, which is periodically saved to a local folder via a volume mount. This means that application data persists even if the application is stopped or, in the worst case, crashes.

This assignment is important because it synthesizes several software engineering concepts. It uses a Python-based Flask server to request a large data set from the web, save it, and manipulate it based on clients' requests. It also uses a popular database system Redis to store data, sequestered within a Docker container. The application itself is intended to be run in another container, decoupling the components and providing consistency and ease-of-use across platforms. These containers can be efficiently started together with a single `docker-compose` command! It also has value from a user perspective, since instead of receiving a complicated XML file of the whole data set, a user can request only what they need, and receive it in JSON.

## Running the Project

It is highly recommended to run the project with `docker-compose` applied to images pulled from [Docker Hub](https://hub.docker.com/repository/docker/ashtonvcole/genome_database/). The user is welcome to pull the source code from GitHub and build their own containers and images, or run the Flask application outside a container with a Python 3 interpreter, but no guarantees are made.

Regardless, an essential, albeit inconvenient step is to personally create a folder on the machine to save Redis data between container runs. When Redis tries to create its own folder, the permissions are ill-set, locking the client out and preventing data from being saved.

### Running with `docker-compose`

For this method, only the Docker images and `docker-compose.yml` are necessary. The user should check that the volume mount specification is set appropriately.

```yml
volumes:
    - ./data:/data
```

The first path should correspond to a user-created directory relative to the YAML file. With that, the images can be deployed as containers with a single line.

```bash
docker-compose up -f
```

The `-d`  tag runs these tasks in the background. If there is a Dockerfile and application source file in the directory, the container will be re-built with this command. Once you are done running the containers, you may stop and remove them with another one-liner.

```bash
docker-compose down
```

### Running without `docker-compose`

Without `docker-compose`, the containers must be run manually. If you are not using the provided application image, you must build it with `docker build `. First, start the Redis container.

```bash
docker run -d -p 6379:6379 -v $(pwd)/data:/data:rw redis:7 --save 1 1
```

This runs the container in the background, binds its port 6379 to that of the machine, sets up a volume mount in the present directory, and saves data periodically.

Then, start the application container.

```bash
docker run -d -p 5000:5000
```

This runs the container in the background and binds its port 5000 to that of the machine.

You may also interpret the application with Python 3, but this is the least recommended, since it prevents version control and sequestering.

## Project Structure

- `Dockerfile` [About](#dockerfile) [File](Dockerfile)
- `docker-compose.yml` [About](#docker-composeyml) [File](docker-compose.yml)
- `genome_database.py` [About](#genome_databasepy) [File](genome_database.py)

### `Dockerfile`

This script is used to build a Docker image, which can excecute the program within a container.

### `docker-compose.yml`

This script is used to optionally build and pull the necessary Docker images, and then run containers from them.

### `genome_database.py`

This script processes all HTTP requests to the API. In addition to code that initializes the server, it contains several functions which execute and return data for a certain endpoint.

## Endpoints

The following endpoints are available to the user. Note that all endpoints, given irregular inputs or error conditions, will return a string message with a 404 status code.

- [`/data`](#data)
- [`/genes`](#genes)
- [`/genes/hgnc_id`](#geneshgnc_id)

### `/data`

#### `POST`

This pulls the source data from online and adds it to the Redis database.

```bash
curl 'http://localhost:5000/data' -X POST
```

```
Data successfully posted
```

#### `GET`

This retrieves all data from the Redis database and returns it in JSON form. Since the data set is large, it is not recommended to get the data directly, but to pipe it into a file.

```bash
curl 'http://localhost:5000/data' -X GET > out.json
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
curl 'http://localhost:5000/data' -X DELETE
```

```
Data successfully deleted
```

### `/genes`

This returns a list of all of the `hgnc_id`'s for each entry in the data set, in JSON form. Since it is unique, this can be considered a primary key for the data set.

```bash
curl 'http://localhost:5000/genes' -X GET > out.json
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
curl 'http://localhost:5000/genes/HGNC:35163' -X GET
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
