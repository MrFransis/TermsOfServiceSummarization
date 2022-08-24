import pandas as pd
import json
import time
import requests
import os.path

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:55.0) Gecko/20100101 Firefox/55.0',
}

def get_ids():
    id_url = "https://api.tosdr.org/all-services/v1/"
    r = requests.get(id_url, headers=headers)
    j = r.json()
    tod_ids = []
    for service in j['parameters']['services']:
        if os.path.isfile('data/tos_' + str(service['id']) + '.json'):
            continue
        tod_ids.append(service['id'])

    return tod_ids

def get_data(ids):
    """
    """
    print("Downloading ToS ...")
    url = 'https://api.tosdr.org/rest-service/v2/'

    for tos_id in ids:
        time.sleep(2)
        r = requests.get(url + str(tos_id) + '.json', headers=headers)

        j = r.json()

        if j['error'] == 193:
            continue

        print(tos_id)

        with open('data/tos_' + str(tos_id) + '.json', 'w') as outfile:
            json.dump(j, outfile)


if __name__ == "__main__":
    ids = get_ids()

    try:
        get_data(ids)

    except Exception as e:
        print(e)