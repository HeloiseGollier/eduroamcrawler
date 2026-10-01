from html import unescape
from lxml import etree
from pathlib import Path
import json
from typing import List

files = list(Path(".").glob("profiles_*.html"))

if not files:
    raise FileNotFoundError("No profile files found")

latest_file = max(files, key=lambda f: f.stat().st_mtime)

print(f"Using: {latest_file}")
with open(latest_file, "r", encoding="utf-8") as f:
    content = unescape(f.read())

entries = content.split('<?xml version="1.0" encoding="utf-8"?>')

def store_file(realms: List, filename: str):
    with open(filename, "w") as fh:
        json.dump(
            realms,
            fh,
            separators=(",", ":"),
            allow_nan=False,
            sort_keys=True,
            ensure_ascii=True,
        )
        fh.write("\r\n")


realms = []
total = 0

for entry in entries:
    entry = entry.strip()

    if not entry:
        continue

    xml = '<?xml version="1.0" encoding="utf-8"?>\n' + entry
    try:
        root = etree.fromstring(xml.encode())
        total += 1
    except Exception:
        continue

    for element in root.findall('./EAPIdentityProvider'):
        if 'RFC4282' in element.attrib['namespace']:
            realms += [element.attrib['ID']]

print(len(realms))
print(total)
store_file(realms, "realms.json")

#We found a list 3939
#4288

# We only record a realm if we get something like this: <EAPIdentityProvider version="1" lang="en" ID="vsup.cz" namespace="urn:RFC4282:realm">
# Sometimes we get an undefined, like this: <EAPIdentityProvider version="1" lang="en" ID="undefined" namespace="urn:undefined">