#!/usr/bin/env python3

import argparse
import json


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        'data_file',
        help='the data file for the feed',
    )
    parser.add_argument(
        '--id',
        help='the feed ID (usually a URL)',
    )
    parser.add_argument(
        '--title',
        help='the feed title',
        default='OpenStack Contributor Community Announcements',
    )
    parser.add_argument(
        '--link',
        help='link for the feed home page',
        default='http://lists.openstack.org/pipermail/openstack-dev/'
    )
    parser.add_argument(
        '--language',
        help='the language for the feed',
        default='en',
    )
    parser.add_argument(
        '--description',
        help='the description for the feed',
        default='Announcements from OpenStack community mailing lists',
    )
    args = parser.parse_args()

    properties = {
        'entries': [],
        'title': args.title,
        'link': args.link,
        'language': args.language,
        'description': args.description,
    }
    if args.id:
        properties['id'] = args.id

    with open(args.data_file, 'w', encoding='utf-8') as f:
        json.dump(properties, f)


if __name__ == '__main__':
    import sys
    sys.exit(main())
