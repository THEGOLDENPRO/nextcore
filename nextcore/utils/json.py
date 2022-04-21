# The MIT License (MIT)
# Copyright (c) 2021-present nextcore developers
#
# Permission is hereby granted, free of charge, to any person obtaining a
# copy of this software and associated documentation files (the "Software"),
# to deal in the Software without restriction, including without limitation
# the rights to use, copy, modify, merge, publish, distribute, sublicense,
# and/or sell copies of the Software, and to permit persons to whom the
# Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
# OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
# DEALINGS IN THE SOFTWARE.

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import Any

try:
    import orjson

    _has_orjson = True
    loads = orjson.loads
except ImportError:
    import json

    _has_orjson = False
    loads = json.loads


__all__ = ("json_loads", "json_dumps")


def json_loads(json: str) -> Any:
    """Loads a json string into a python object.

    Parameters
    ----------
    json: :class:`str`
        The json string to load.
    """
    return loads(json)


def json_dumps(to_dump: Any) -> str:
    """Dumps a python object into a json string.

    Parameters
    ----------
    to_dump: :class:`typing.Any`
        The python object to dump.
    """
    if _has_orjson:
        # Seems like pyright has some issues with having two modules under the same name.
        return orjson.dumps(to_dump).decode("utf-8")
    return json.dumps(to_dump)
