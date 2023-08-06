# notiRSS

Simple CLI RSS real-time notifier via webhook.

## Installation
From PyPi:

`pip install notirss`

From Github:

`pip install git+https://github.com/scratchmex/notirss#egg=notirss`

## Usage

```console
❯ notirss -h
usage: notirss [-h] -f FEED -c ENTRIES [-x EXTRACT] -w WEBHOOK [-t TIME] [-v]

Simple CLI RSS real-time notifier via webhook.

optional arguments:
  -h, --help            show this help message and exit
  -f FEED, --feed FEED  the RSS feed URL to check
  -c ENTRIES, --entries ENTRIES
                        amount of entries returned by the feed
  -x EXTRACT, --extract EXTRACT
                        data mapping in JSON format to extract from RSS feed, default all data
  -w WEBHOOK, --webhook WEBHOOK
                        webhook url to GET when new item/s found
  -t TIME, --time TIME  periodic time interval to check in seconds
  -v, --verbose         set logging level to DEBUG
```