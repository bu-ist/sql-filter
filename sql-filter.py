#!/usr/bin/env python
# encoding: utf-8
"""
sql-filter.py

Created by Niall Kavanagh on 3/20/2014
"""

from __future__ import print_function
import argparse
import sqlparse
import os
import sys


def is_token_allowed(token):
    if token.value.upper() == 'SLEEP':
        return False
    else:
        return True


def filter_token(token):
    if token.is_group():
        child = token.token_first()

        # to hold children that aren't blacklisted
        good_children = []

        while child:
            filtered_child = filter_token(child)
            if filtered_child is not None:
                good_children.append(filtered_child.value)

            idx = token.token_index(child)
            child = token.token_next(idx, skip_ws=True)

        if len(good_children) > 0:
            token = sqlparse.sql.Token(None, ' '.join(good_children))
            return token
        else:
            return None
    else:
        if is_token_allowed(token):
            return token
        else:
            return None


def main():
    # command line args
    parser = argparse.ArgumentParser(description='Filters blacklisted \
                                     functions and keywords from a SQL \
                                     query.')

    parser.add_argument('filename', help='the filename containing the SQL \
                        query')

    parser.add_argument('--blacklist', default='blacklist.txt',
                        help='the filename contain a list of \
                        blacklisted functions and keywords')

    args = parser.parse_args()

    if not os.path.isfile(args.filename):
        print('File not found: {0}'.format(args.filename),
              file=sys.stderr)
        sys.exit(1)

    if not os.path.isfile(args.blacklist):
        print('Blacklist not found: {0}'.format(args.blacklist),
              file=sys.stderr)

    original_sql = ''
    with open(args.filename, 'r') as sql_file:
        original_sql = sql_file.read().replace('\n', '')

    statements = sqlparse.parse(original_sql)

    for statement in statements:
        print('{0}: {1}'.format(statement.get_type(), statement))

        filtered_parts = []

        token = statement.token_first()

        while token:
            filtered_token = filter_token(token)
            if filtered_token is not None:
                filtered_parts.append(filtered_token.value)

            idx = statement.token_index(token)
            token = statement.token_next(idx, skip_ws=True)

        filtered_query = ''

        if len(filtered_parts) > 0:
            filtered_query = ' '.join(filtered_parts)

        print('Filtered: {0}'.format(filtered_query))

if __name__ == '__main__':
    main()
