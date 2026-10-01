import json
from typing import List
from datetime import datetime
import requests


timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
filename = f"profiles_{timestamp}.html"

with open('discovery.json') as f:
    discovery = json.load(f)

    #for i in range(0, 3):
    for i in range(0,  len(discovery['instances'])):
        if i%50 == 0:
            print(f"{i} profiles discovered so far (out of {len(discovery['instances'])})")
        try:
            if discovery['instances'][i]['profiles'][0].get('authorization_endpoint') is not None:
                continue
            r = requests.get(discovery['instances'][i]['profiles'][0]['eapconfig_endpoint'])
            with open(filename, "a", encoding="utf-8") as f:
                f.write(r.text)
        except KeyError:
            continue

