#!/usr/bin/env python3

import argparse
import json

from feedgen.feed import FeedGenerator


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        'data_file',
        help='the data file for the feed',
    )
    parser.add_argument(
        'rss_file',
        help='the output file to produce',
    )
    args = parser.parse_args()

    with open(args.data_file, 'r', encoding='utf-8') as f:
        data = json.loads(f.read())

    gen = FeedGenerator()
    if data.get('id'):
        gen.id(data['id'])
    gen.title(data['title'])
    gen.link(href=data['link'])
    gen.language(data['language'])
    gen.description(data['description'])

    for e in data['entries']:
        entry = gen.add_entry()
        entry.id(e['url'])
        entry.title(e['title'])
        entry.link(href=e['url'])
        entry.content(e['body'])
        entry.published(e['date'])

    gen.rss_file(args.rss_file)


if __name__ == '__main__':
    import sys
    sys.exit(main())
