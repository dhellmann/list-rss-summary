#!/usr/bin/env python3

import argparse
import json
import re

from bs4 import BeautifulSoup
import requests

START = re.compile('<!--beginarticle-->')
END = re.compile('<!--endarticle-->')

TITLE_CLEANUP = re.compile('\[openstack-dev\]')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        'data_file',
        help='the data file for the feed',
    )
    parser.add_argument(
        'url',
        help='the URL to add',
    )
    args = parser.parse_args()

    try:
        with open(args.data_file, 'r', encoding='utf-8') as f:
            data = json.loads(f.read())
    except FileNotFoundError:
        data = []

    for e in data:
        if e['url'] == args.url:
            print('ERROR: Already have {}'.format(args.url))
            return 1

    page = requests.get(args.url)

    soup = BeautifulSoup(page.text, 'lxml')

    # Find the title text and clean it up
    title = list(soup.find_all('h1'))[1].text
    title = TITLE_CLEANUP.sub('', title).strip()

    start = START.search(page.text)
    end = END.search(page.text)

    body = page.text[start.span()[1]:end.span()[0]].strip()

    entry = {
        'url': args.url,
        'body': body,
        'title': title,
    }
    data.append(entry)
    with open(args.data_file, 'w', encoding='utf-8') as f:
        f.write(json.dumps(data))


if __name__ == '__main__':
    import sys
    sys.exit(main())
