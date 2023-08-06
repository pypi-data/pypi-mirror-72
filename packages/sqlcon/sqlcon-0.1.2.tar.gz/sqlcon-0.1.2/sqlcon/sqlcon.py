import io
import pathlib
import sys

__all__ = ["process", "joinwith", "indented_joinwith"]


def _get_n_leading_spaces(line: str):
    """Return number of spaces before the first non-space character."""
    return len(line) - len(line.lstrip(" "))


def _strip(a: str):
    a = a.rstrip(" ")
    if a and a[0] == "\n":
        a = a[1:]
    if a and a[-1] == "\n":
        a = a[:-1]
    return a


def _process(sqlcons, output_file, i=0, spaces="    "):

    # Use an inner function for recursive calling in a closure.
    def f(sqlcons):
        nonlocal i
        if isinstance(sqlcons, str):
            lines = _strip(sqlcons).splitlines()
            if len(lines) > 0:
                first_line_lead = _get_n_leading_spaces(lines[0])
                for line in lines:
                    line = line.rstrip()
                    if line:
                        line = (i * spaces + line)[first_line_lead:]
                        output_file.write(line)
                    output_file.write("\n")
                i = _get_n_leading_spaces(line) // len(spaces)
            else:
                output_file.write("\n")
        elif isinstance(sqlcons, int):
            i += sqlcons
        else:
            # Assume some kind of iterable - a list, tuple, or generator
            for s in sqlcons:
                f(s)

    f(sqlcons)


def process(sqlcons, output=None, i=0, spaces="    "):
    """Process "sqlcons" into SQL.

    If `output` is None then return a string.
    If `output` satisfies the file protocol than write to it directly (and return None).
    If `output` == "stdout" then write to stdout (and return None).
    If `output` is a pathlib object or str then try to open a file of that name
      and write to it (and return None).

    """
    if output == "stdout":
        output_file = sys.stdout
        _process(sqlcons, output_file, i=i, spaces=spaces)
    elif output is None:
        output_file = io.StringIO()
        _process(sqlcons, output_file, i=i, spaces=spaces)
        return output_file.getvalue()
    elif isinstance(output, pathlib.Path):
        with output.open("w") as output_file:
            _process(sqlcons, output_file, i=i, spaces=spaces)
    elif isinstance(output, str):
        with pathlib.Path(output).open("w") as output_file:
            _process(sqlcons, output_file, i=i, spaces=spaces)


def _add_trailing(thing, trailing_text: str):
    if isinstance(thing, str):
        return _strip(thing) + trailing_text
    things = list(thing)
    if len(things) > 0:
        things[-1] = _add_trailing(things[-1], trailing_text)
    return things


def joinwith(a_list, include_last=False, separator=","):
    """Return new sqlcons list joined with commas at end of all text items except for the last.

    Optionally use a different separator or include the separator on the last item too

    """
    a_list = list(a_list)
    if include_last:
        return [_add_trailing(a, separator) for a in a_list]
    else:
        if len(a_list) > 0:
            head = [_add_trailing(a, separator) for a in a_list[:-1]]
            tail = [_add_trailing(a_list[-1], "")]  # Ensure we still use _strip
            return head + tail
        else:
            return []


def indented_joinwith(a_list, include_last=False, separator=","):
    """Same as `joinwith` but prepended with an indent and appended with an outdent."""
    return 1, joinwith(a_list, include_last=include_last, separator=separator), -1
