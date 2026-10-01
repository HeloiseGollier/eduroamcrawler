# EduroamCrawler

This repository is a fork from [cattenbak](https://github.com/geteduroam/cattenbak), a scraper for cat.eduroam.org that generates discovery files for geteduroam. We have extended the code to collect PEAP-specific statistics. This extension was made in the context of the paper *Looking through the PEAPhole: Security Analysis of PEAP in Eduroam and Enterprise Wi-Fi* to be published at NDSS 2027.

## Eduroam profile statistics

Crawling Eduroam profiles to find how many use anonymous identities, retrieve realms, and find which EAP types are most frequently used.

    cd eduroamcrawler
    python3 cattenbak.py
    python3 profilecrawler.py
    python3 anonymousidentityfinder.py
    python3 retrieve_realms.py
    python3 eap_statistics.py


## License

See COPYING
