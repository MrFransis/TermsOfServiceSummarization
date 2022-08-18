import pandas as pd
import json
import time
import requests

url = 'https://api.tosdr.org/rest-service/v2/'
headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:55.0) Gecko/20100101 Firefox/55.0',
}

def get_data(start_id):
    """
    """
    print("Downloading ToS ...")

    while start_id <= 2000:
        time.sleep(2)
        r = requests.get(url + str(start_id) + '.json', headers=headers)

        j = r.json()

        if j['error'] == 193:
            continue

        print(start_id)

        with open('data/tos_' + str(start_id) + '.json', 'w') as outfile:
            json.dump(j, outfile)

        start_id = start_id + 1


if __name__ == "__main__":
    start_id = 332

    try:
        get_data(start_id)

    except Exception as e:
        print(e)