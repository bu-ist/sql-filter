"""
Implementation for the SQL filtering
"""

from sqlparse import sql


def filter_token_group(group, blacklisted_tokens):
    """
    Filters a list of tokens
    """
    filtered_group = group
    child = group.token_first()

    # to hold children that aren't blacklisted
    good_children = []

    was_filtered = False

    while child:
        filtered_child = filter_token(child, blacklisted_tokens)

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
            tokens = ' '.join(unicode(tok) for tok in good_children)
            filtered_group = sql.Token(None, tokens)
        else:
            filtered_group = None

    return filtered_group


def filter_token(token, blacklisted_tokens):
    """
    Filter a single token
    """
    filtered_token = token

    if token.is_group():
        filtered_token = filter_token_group(token, blacklisted_tokens)
    elif unicode(token).upper() in (s.upper() for s in blacklisted_tokens):
        filtered_token = None

    return filtered_token


def filter_statement(statement, blacklisted_tokens):
    """
    Filters a single statement
    """
    was_filtered = False
    filtered_parts = []

    token = statement.token_first()

    while token:
        filtered_token = filter_token(token, blacklisted_tokens)

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
