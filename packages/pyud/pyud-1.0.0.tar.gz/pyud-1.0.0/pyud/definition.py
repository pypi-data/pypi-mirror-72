# -*- coding: utf-8 -*-
"""
pyud.definition
Copyright (c) 2020 William Lee

This file is part of pyud.

pyud is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

pyud is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with pyud.  If not, see <https://www.gnu.org/licenses/>.
"""

import json
from datetime import datetime as dt
from typing import Any, List


class Definition:
    """
    Represents an Urban Dictionary definition

    This class is not intended to be instantiated directly.
    It is preferably obtained using either one
    of :class:`Client` or :class:`AsyncClient`, and using one
    of the defined API wrapper methods/coroutines to retrieve definitions
    from the API.

    .. note::

        Any additional attributes that may be provided in the future by the API
        are also added to the instance, but they are provided as is,
        and are not processed in any way. Future versions may be support
        any added attributes.

    .. note::

        The :attr:`current_vote` attribute is not included 
        as a required attribute, as it does not contain any meaningful information.

    .. attribute:: defid

        The ID of the definition

        :type: int

    .. attribute:: word

        The term being defined

        :type: str

    .. attribute:: definition

        The definition description

        :type: str

    .. attribute:: author

        The author of the definition

        :type: str

    .. attribute:: thumbs_up

        The number of upvotes on the definition

        :type: int

    .. attribute:: thumbs_down

        The number of downvotes on the definition

        :type: int

    .. attribute:: example

        An example usage of the term

        :type: str

    .. attribute:: permalink

        A permalink to the definition

        :type: str

    .. attribute:: written_on

        The date that the definition was written

        :type: datetime.datetime
    """
    def __init__(
        self,
        *,
        defid: int,
        word: str,
        definition: str,
        author: str,
        thumbs_up: int,
        thumbs_down: int,
        example: str,
        permalink: str,
        sound_urls: List[str],
        written_on: str,
        **attrs: Any,
    ):
        """
        Instantiates an instance of an Urban Dictionary definition
        """
        self.defid = defid
        self.word = word
        self.definition = definition
        self.author = author
        self.thumbs_up = thumbs_up
        self.thumbs_down = thumbs_down
        self.example = example
        self.permalink = permalink
        self.sound_urls = sound_urls

        # Parses the RFC 3339 timestring to a naive datetime object
        self.written_on = dt.strptime(written_on, "%Y-%m-%dT%H:%M:%S.%fZ")

        # Excess attributes are added
        for name, value in attrs.items():
            setattr(self, name, value)
