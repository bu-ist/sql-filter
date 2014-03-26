"""
Filters blacklisted tokens from a SQL statement.

Created by Niall Kavanagh <ntk@bu.edu> on 3/26/2014
"""

__version__ = '0.1.0'

from sqlparse import format
from sqlparse import parse
from sqlfilter import filter


def filter_sql(sql, blacklisted_tokens, format_filtered=True):
    statements = parse(sql.replace('\n', ' '))
    was_filtered = False
    filtered_sql = ''

    for statement in statements:
        filtered_statement = filter.filter_statement(statement,
                                                     blacklisted_tokens)

        if filtered_statement != statement:
            was_filtered = True
            filtered_sql += filtered_statement
        else:
            filtered_sql += str(statement)

    if was_filtered:
        if format_filtered:
            filtered_sql = format(filtered_sql,
                                  reindent=True,
                                  keyword_case='upper')

        return filtered_sql
    else:
        return sql
