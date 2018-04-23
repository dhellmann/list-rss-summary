#!/usr/bin/env python3

import argparse
import json

from bs4 import BeautifulSoup
import requests


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        'data_file',
        help='the data file for the feed',
    )
    args = parser.parse_args()

    with open(args.data_file, 'r', encoding='utf-8') as f:
        data = json.loads(f.read())

    for entry in data['entries']:
        if 'author' not in entry:
            page = requests.get(entry['url'])
            soup = BeautifulSoup(page.text, 'lxml')
            author = soup.find_all('b')[0].text.strip()
            entry['author'] = {'name': author}
            print('Adding author {} to {!r}'.format(author, entry['title']))
        if 'email' not in entry['author']:
            entry['author']['email'] = 'noreply@openstack.org'

    with open(args.data_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2)


if __name__ == '__main__':
    import sys
    sys.exit(main())
