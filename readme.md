# Download Yukon Government contract data

Very rough data downloader to run against the Yukon Government contract registry.

https://service.yukon.ca/apps/contract-registry/

## Requirements

- Python 
- [Poetry](https://python-poetry.org)
- [Scrapy](https://docs.scrapy.org/en/latest/index.html)

## Installation

```
poetry install
```

## Run

```
poetry shell
scrapy runspider contracts.py -o contract.jsonl
```
## Note

This is just a hastily assembled test script. It should be improved

- define an Feed exporter
- use the Scrapy recommended project structure
- parse contract details pages for additional information