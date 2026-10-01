from html import unescape
from lxml import etree
from pathlib import Path

files = list(Path(".").glob("profiles_*.html"))

if not files:
    raise FileNotFoundError("No profile files found, run profilecrawler.py first.")

latest_file = max(files, key=lambda f: f.stat().st_mtime)

print(f"Using: {latest_file}")
with open(latest_file, "r", encoding="utf-8") as f:
    content = unescape(f.read())



entries = content.split('<?xml version="1.0" encoding="utf-8"?>')

count = 0
total = 0
peap_profiles = 0

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

    # Check whether this provider has EAP type 26
    has_type25 = False

    for auth in root.xpath(".//AuthenticationMethod"):
        if auth.findtext("./EAPMethod/Type") == "25":
            has_type25 = True
            peap_profiles += 1

            if auth.find("./ClientSideCredential/OuterIdentity") is not None:
                count += 1

            break

print(f"Processed {total} XML entries")
print(f"Type 25 + OuterIdentity: {count} out of {peap_profiles} PEAP profiles")
