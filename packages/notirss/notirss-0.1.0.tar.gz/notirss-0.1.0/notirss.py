import argparse as ap
import feedparser as fp
import logging as log
import threading as th
import requests
import json

from time import sleep
from collections import deque
from requests.exceptions import ConnectionError


def callback(data, url):
    log.debug('Sending data to callback')
    try:
        r = requests.post(url, json=data)
    except ConnectionError as e:
        log.error(f'Error sending [{data}] -> [{str(e)}]')
        return

    if r.status_code != 200:
        log.error(f'Not ok status code -> {r.status_code}[{r.text}]')  # noqa
    
    log.info('Webhook GET ok')

    return


def check(url, etag):
    log.debug('Lets check')
    r = fp.parse(url, etag=etag)

    if r.bozo:
        log.error(str(r.bozo_exception))
        return [], etag
        # raise r.bozo_exception

    etag = r.etag

    if not r.entries:
        log.debug('Nothing new')
        return [], etag

    log.debug('New entries')

    return r.entries, etag


def cli():
    par = ap.ArgumentParser(
        description='Simple CLI RSS real-time notifier via webhook.')
    par.add_argument(
        '-f', '--feed',
        help='the RSS feed URL to check',
        required=True
    )
    par.add_argument(
        '-c', '--entries',
        help='amount of entries returned by the feed',
        required=True,
        type=int
    )
    par.add_argument(
        '-x', '--extract',
        help='data mapping in JSON format to extract from RSS feed, default all data',
        type=json.loads
    )
    par.add_argument(
        '-w', '--webhook',
        help='webhook url to GET when new item/s found',
        required=True
    )
    par.add_argument(
        '-t', '--time',
        help='periodic time interval to check in seconds',
        default='10',
        type=int
    )
    par.add_argument(
        '-v', '--verbose',
        help='set logging level to DEBUG',
        action='store_true'
    )

    args = par.parse_args()
    loglev = log.DEBUG if args.verbose else log.INFO
    log.basicConfig(
        format='%(asctime)s:%(name)s:%(levelname)s:%(funcName)s:%(message)s',
        level=loglev
    )

    etag = ''
    entries = deque(maxlen=args.entries)

    while True:
        data, etag = check(args.feed, etag)

        if not data:
            sleep(args.time)
            continue
        
        if args.extract:
            data = [
                tuple((nk, x[k]) for k, nk in args.extract.items())
                for x in data
            ]
        else:
            data = [tuple(x.items()) for x in data]

        new = [x for x in reversed(data) if x not in entries]
        log.info(f'{len(new)} new entries')

        # don't send initial data
        if not entries:
            log.info('Initial data, not sending')
            entries.extend(new)
            continue

        for x in new:
            entries.append(x)
            t = th.Thread(
                target=callback,
                args=({k : v for k, v in x}, args.webhook)
            )
            t.start()


if __name__ == "__main__":
    cli()
