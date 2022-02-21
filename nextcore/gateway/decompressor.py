# The MIT License (MIT)
# Copyright (c) 2021-present nextsnake developers

# Permission is hereby granted, free of charge, to any person obtaining a
# copy of this software and associated documentation files (the "Software"),
# to deal in the Software without restriction, including without limitation
# the rights to use, copy, modify, merge, publish, distribute, sublicense,
# and/or sell copies of the Software, and to permit persons to whom the
# Software is furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
# OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
# DEALINGS IN THE SOFTWARE.
from __future__ import annotations

from zlib import decompressobj

ZLIB_SUFFIX = b"\x00\x00\xff\xff"


class Decompressor:
    """
    A simple wrapper around zlib to handle spreading a payload over multiple messages
    """

    __slots__ = ("_decompressor", "_buffer")

    def __init__(self) -> None:
        self._decompressor = decompressobj()
        self._buffer: bytearray = bytearray()

    def decompress(self, data: bytes) -> bytes | None:
        """
        Decompress data

        Returns:
            bytes | None: decompressed data. None if the payload is incomplete
        Raise:
            ValueError: if the data is not compressed
        """
        self._buffer.extend(data)

        if len(data) < 4 or data[-4:] != ZLIB_SUFFIX:
            # Not a full payload, try again next time
            return None

        try:
            data = self._decompressor.decompress(data)
        except ValueError:
            raise ValueError("Data is corrupted. Please void all zlib context.")

        # If successful, clear the pending data.
        self._buffer = bytearray()
        return data
