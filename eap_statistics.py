from pathlib import Path
from html import unescape
from collections import Counter, defaultdict
from lxml import etree

# Find newest crawl file
latest_file = max(
    Path(".").glob("profiles_*.html"),
    key=lambda f: f.name
)

with open(latest_file, "r", encoding="utf-8") as f:
    content = unescape(f.read())

entries = content.split('<?xml version="1.0" encoding="utf-8"?>')

# Statistics
eap_counts = Counter()
inner_counts = defaultdict(Counter)

total_profiles = 0

for entry in entries:
    entry = entry.strip()
    if not entry:
        continue
    xml = '<?xml version="1.0" encoding="utf-8"?>\n' + entry
    try:
        root = etree.fromstring(xml.encode())
        total_profiles += 1
    except Exception:
        continue


    for auth in root.findall(".//AuthenticationMethod"):
        eap_type = auth.findtext("./EAPMethod/Type")
        if eap_type is None:
            continue

        eap_counts[eap_type] += 1
        # Find inner authentication method
        inner = auth.find("./InnerAuthenticationMethod")

        if inner is not None:
            inner_type = None
            # PEAP/MSCHAPv2 style
            if inner.find("./NonEAPAuthMethod/Type") is not None:
                inner_type = (
                    "NonEAP:"
                    + inner.findtext("./NonEAPAuthMethod/Type")
                )
            # EAP-inside-EAP style
            elif inner.find("./EAPMethod/Type") is not None:
                inner_type = (
                    "EAP:"
                    + inner.findtext("./EAPMethod/Type")
                )

            if inner_type:
                inner_counts[eap_type][inner_type] += 1



print(f"Profiles processed: {total_profiles}")

print("\nEAP Method Counts")
print("=================")

for eap_type, count in sorted(
    eap_counts.items(),
    key=lambda x: int(x[0])
):
    print(f"EAP {eap_type}: {count}")

print("\nInner Authentication Methods")
print("============================")

for eap_type, counter in sorted(
    inner_counts.items(),
    key=lambda x: int(x[0])
):
    print(f"\nEAP {eap_type}")

    for inner_type, count in counter.most_common():
        print(f"  {inner_type}: {count}")