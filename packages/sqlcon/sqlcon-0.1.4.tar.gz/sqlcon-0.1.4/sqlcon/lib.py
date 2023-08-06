import re
import string

__all__ = ["make_valid_name", "is_invalid_name", "single_quote", "double_quote"]


def make_valid_name(text):
    numbers = "0123456789"
    valid_chars = set(numbers + string.ascii_lowercase + string.ascii_uppercase + "_")
    # Remove leading numbers
    text = text.lstrip(numbers)
    # Replace space with underscore
    text = text.replace(" ", "_")
    # Replace dash with underscore
    text = text.replace("-", "_")
    # Only include valid chars
    return "".join(a for a in text if a in valid_chars)


def is_invalid_name(name, regex=r"^[A-Za-z_]+[A-Za-z_0-9]*$"):
    return re.match(regex, name) is None


def single_quote(text):
    """Safely add single quotes around given text e.g. to make PostgreSQL string literals.

    Identical to pglib's `PQescapeInternal` with `as_ident = False`. See:
        https://github.com/postgres/postgres/blob/master/src/interfaces/libpq/fe-exec.c#L3443

    That also makes it the same as the PostgreSQL function `quote_literal`.

    Assume Python is working with the same string encoding as PostgreSQL e.g.
    both UTF8.

    """
    text = str(text)
    quote = "'"
    backslash = "\\"
    opening = f" E{quote}" if backslash in text else quote
    closing = quote
    text = text.replace(backslash, backslash * 2)  # Double up every backslash
    text = text.replace(quote, quote * 2)  # Double up every quote
    return f"{opening}{text}{closing}"


def double_quote(text):
    """Safely add double quotes around given text e.g. to make PostgreSQL identifiers.

    Identical to pglib's `PQescapeInternal` with `as_ident = True`. See:
        https://github.com/postgres/postgres/blob/master/src/interfaces/libpq/fe-exec.c#L3443

    That also makes it the same as the PostgreSQL function `quote_ident`, but
    with the difference that it is always quoted.

    Assume Python is working with the same string encoding as PostgreSQL e.g.
    both UTF8.

    """
    text = str(text)
    quote = '"'
    opening = quote
    closing = quote
    text = text.replace(quote, quote * 2)  # Double up every quote
    return f"{opening}{text}{closing}"
