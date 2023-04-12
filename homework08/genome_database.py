import redis
import requests
from flask import Flask, request
import os





app = Flask(__name__)
source_url = 'https://ftp.ebi.ac.uk/pub/databases/genenames/hgnc/json/hgnc_complete_set.json'





def get_redis_client():
    """Returns the Redis database client.

    This function returns a Redis object permitting access to a Redis client
    via 127.0.0.1:6379. The object specifically manipulates database 0. It is
    set to decode responses from the client from bytes to Python strings.
    """
    redis_host = os.environ.get('REDIS_IP')
    if not redis_host:
        raise Exception()
    return redis.Redis(host = redis_host, port = 6379, db = 0, decode_responses = True)





@app.route('/data', methods = ['GET', 'POST', 'DELETE'])
def data():
    """/data endpoint

    This function either returns all data in the database, updates the database
    with the latest source data, or clears the database, depending on if the
    HTTP request method is GET, POST, or DELETE, respectively.

    Args:
        None

    Returns:
        If the method is GET, a list of dictionaries representing each entry in
            the database. If there is an error, a descriptive string will be
            returned with a 500 status code. Note that sparse attributes are
            excluded.
        If the method is SET, a text message informing the user of success. If
            there is an error, a descriptive string will be returned with a 500
            status code.
        If the method is DELETE, a text message informing the user of success.
            If there is an error, a descriptive string will be returned with a
            500 status code.
    """
    global rd, source_url
    if request.method == 'GET':
        try:
            data = []
            keys = rd.keys()
            for key in keys:
                data.append(rd.hgetall(key))
            return data
        except Exception as e:
            print(f'ERROR: unable to get data\n{e}')
            return f'ERROR: unable to get data', 500
    elif request.method == 'POST':
        try:
            the_json = requests.get(url = source_url).json()
            data = the_json['response']['docs']
            for item in data:
                key = f'{item["hgnc_id"]}'
                subkeys = item.keys()
                for subkey in subkeys:
                    if type(item[subkey]) == list:
                        listitem = ''
                        for j in range(0, len(item[subkey]) - 1):
                            listitem = f'{listitem}{item[subkey][j]}|'
                        listitem = f'{listitem}{item[subkey][len(item[subkey]) - 1]}'
                        rd.hset(key, subkey, listitem)
                    else:
                        rd.hset(key, subkey, item[subkey])
            return 'Data successfully posted', 200
        except Exception as e:
            print(f'ERROR: unable to post data\n{e}')
            return f'ERROR: unable to post data', 500
    elif request.method == 'DELETE':
        try:
            rd.flushdb()
            return 'Data successfully deleted', 200
        except Exception as e:
            print(f'ERROR: unable to delete data\n{e}')
            return f'ERROR: unable to delete data', 500





@app.route('/genes', methods = ['GET'])
def genes():
    """/genes endpoint

    This function returns all of the gene IDs, i.e. hgnc_id, in the set.

    Args:
        None

    Returns:
        A list of strings, the hgnc_id of each entry.
    """
    global rd
    try:
        return rd.keys()
    except Exception as e:
        print(f'ERROR: unable to get gene ID\'s\n{e}')
        return f'ERROR: unable to get gene ID\'s', 500





@app.route('/genes/<string:hgnc_id>', methods = ['GET'])
def genes_gene_id(hgnc_id: str):
    """/genes/<string:hgnc_id> endpoint

    This function returns all of the data for a gene specified by its hgnc_id.
    Note that sparse attributes are excluded.

    Args:
        hgnc_id: A string of the hgnc_id of the desired gene.

    Returns:
        A dictionary holding the attributes of a gene. Note that sparse
        attributes are excluded.
    """
    global rd
    try:
        item = rd.hgetall(hgnc_id)
        if len(item) > 0:
            return item
        else:
            return f'ERROR: Gene {hgnc_id} not found.', 404
    except Exception as e:
        print(f'ERROR: unable to get gene.\n{e}')
        return f'ERROR: unable to get gene.', 500





rd = get_redis_client()

if __name__ == '__main__':
    app.run(host = '0.0.0.0', debug = True)
