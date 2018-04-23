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
        print('ERROR: Could not read feed data file {}'.format(args.data_file))
        return 1

    for e in data['entries']:
        if e['url'] == args.url:
            print('ERROR: Already have {}'.format(args.url))
            return 1

    page = requests.get(args.url)

    soup = BeautifulSoup(page.text, 'lxml')

    # Find the title text and clean it up
    title = list(soup.find_all('h1'))[1].text
    title = TITLE_CLEANUP.sub('', title).strip()

    # Get the whole body, including the pre tags.
    start = START.search(page.text)
    end = END.search(page.text)
    body = page.text[start.span()[1]:end.span()[0]].strip()

    # Find the date
    date_str = soup.find_all('i')[0].text.strip()

    entry = {
        'url': args.url,
        'body': body,
        'title': title,
        'date': date_str,
    }
    data['entries'].append(entry)
    print('There are now {} entries'.format(len(data['entries']))
    with open(args.data_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2)


if __name__ == '__main__':
    import sys
    sys.exit(main())
