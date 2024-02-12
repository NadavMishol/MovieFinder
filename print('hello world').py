import gzip
import shutil
import requests
import csv
from io import StringIO

URL = 'https://datasets.imdbws.com/title.basics.tsv.gz'
output_file = 'title.basics.tsv'

response = requests.get(URL)

with open('name.basics.tsv.gz', 'wb') as f:
    f.write(response.content)

# Unzip the file
with gzip.open('name.basics.tsv.gz', 'rb') as f_in:
    with open(output_file, 'wb') as f_out:
        shutil.copyfileobj(f_in, f_out)

with open(output_file, 'r', encoding='utf-8') as file:
    reader = csv.reader(file, delimiter='\t')
    for _ in range(10):
        print(next(reader))