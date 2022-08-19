import json
import os
import pandas as pd

path_to_json = 'data/'
json_files = [pos_json for pos_json in os.listdir(path_to_json) if pos_json.endswith('.json')]
print(json_files)

data = []

for json_file in json_files:
    with open(path_to_json + json_file, 'r') as f:
        data.append(json.load(f))

reviewed_terms = []
for doc in data:
    if doc['parameters']['is_comprehensively_reviewed'] is True:
        reviewed_terms.append(doc)

# Create the summaries by merging the quotes
final_data = []

for doc in reviewed_terms:
    legal_contracts = {}

    for point in doc['parameters']['points']:
        if point['quoteStart'] is not None and point['quoteText'] is not None:
            legal_contracts.setdefault(point['document_id'], []).append(point)

    for doc_id, value in legal_contracts.items():
        legal_contracts[doc_id] = sorted(value, key=lambda i: i['quoteStart'])

        plain_text = ""
        summary = ""
        for point in legal_contracts[doc_id]:
            plain_text += " " + point['quoteText']
            summary += ". " + point['title']

        final_data.append([plain_text, summary])

df = pd.DataFrame(final_data, columns=['plain_text', 'summary'])
df.to_json('dataset.json', orient='records', lines=True)