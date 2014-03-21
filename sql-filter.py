#!/usr/bin/env python
# encoding: utf-8
"""
sql-filter.py

Exits cleanly if no filtering required
Exits with errno=1 if query was filtered
Exits with errno=2 if something else went wrong

Created by Niall Kavanagh on 3/20/2014
"""

from __future__ import print_function
import argparse
import sqlparse
import os
import sys

# global to hold blacklist
blacklisted_tokens = []


def is_token_allowed(token):
    global blacklisted_tokens

    is_allowed = True

    for invalid_token in blacklisted_tokens:
        if token.value.upper() == invalid_token.upper():
            is_allowed = False

    return is_allowed


def filter_token_group(group):
    filtered_group = group
    child = group.token_first()

    # to hold children that aren't blacklisted
    good_children = []

    was_filtered = False

    while child:
        filtered_child = filter_token(child)

        if filtered_child:
            good_children.append(filtered_child)
            if filtered_child.value != child.value:
                was_filtered = True
        else:
            was_filtered = True

        idx = group.token_index(child)
        child = group.token_next(idx, skip_ws=True)

    if was_filtered:
        if len(good_children) > 0:
            # tokens as strings
            tokens = ' '.join(str(tok) for tok in good_children)
            filtered_group = sqlparse.sql.Token(None, tokens)
        else:
            filtered_group = None

    return filtered_group


def filter_token(token):
    filtered_token = token

    if token.is_group():
        filtered_token = filter_token_group(token)
    elif not is_token_allowed(token):
        filtered_token = None

    return filtered_token


def filter_statement(statement):
    was_filtered = False
    filtered_parts = []

    token = statement.token_first()

    while token:
        filtered_token = filter_token(token)

        if token != filtered_token:
            was_filtered = True

        if filtered_token is not None:
            filtered_parts.append(filtered_token.value)

        idx = statement.token_index(token)
        token = statement.token_next(idx, skip_ws=True)

    filtered_sql = ''

    if len(filtered_parts) > 0:
        filtered_sql = ' '.join(filtered_parts)

    if was_filtered:
        return filtered_sql
    else:
        return statement


def main():
    global blacklisted_tokens

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
        sys.exit(2)

    if not os.path.isfile(args.blacklist):
        print('Blacklist not found: {0}'.format(args.blacklist),
              file=sys.stderr)
        sys.exit(2)

    # load the blacklist
    with open(args.blacklist) as f:
        blacklisted_tokens = f.read().splitlines()

    # parse the SQL
    original_sql = ''
    with open(args.filename, 'r') as sql_file:
        original_sql = sql_file.read().replace('\n', '')

    statements = sqlparse.parse(original_sql)
    was_filtered = False

    for statement in statements:
        filtered_statement = filter_statement(statement)

        if filtered_statement != statement:
            print(filtered_statement)
            was_filtered = True
        else:
            print(statement)

    if was_filtered:
        # we filtered, exit code 1
        sys.exit(1)
    else:
        # exit cleanly
        sys.exit(0)

if __name__ == '__main__':
    main()
