"""LICENSE
Copyright 2015 Hermann Krumrey <hermann@krumreyh.com>

This file is part of manga-dl.

manga-dl is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

manga-dl is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with manga-dl.  If not, see <http://www.gnu.org/licenses/>.
LICENSE"""

import os
import shutil
import logging
from puffotter.os import makedirs
from typing import Callable, List
from typing import Optional
from subprocess import Popen


class Chapter:
    """
    Class that models a manga chapter
    """

    def __init__(
            self,
            url: str,
            language: str,
            series_name: str,
            chapter_number: str,
            destination_dir: str,
            _format: str,
            page_load_callback: Callable[[str], List[str]]
    ):
        """
        Initializes the manga chapter
        :param url: The URL used to fetch page image URLs
        :param language: The language of the chapter
        :param series_name: The name of the series
        :param chapter_number: The chapter number of this chapter
        :param destination_dir: The destination directory in which to store
                                downloaded files by default
        :param _format: The format in which to store the chapter when
                        downloading by default
        :param page_load_callback:
        """
        self.logger = logging.getLogger(self.__class__.__name__)
        self.url = url
        self.language = language
        self.series_name = series_name
        self.chapter_number = chapter_number
        self.destination_dir = destination_dir
        self.format = _format
        self._page_load_callback = page_load_callback
        self._pages = []

    @property
    def name(self) -> str:
        """
        :return: The name of the chapter
        """
        return "{} - Chapter {}".format(self.series_name, self.chapter_number)

    @property
    def pages(self) -> List[str]:
        """
        Lazy-loads the URLs of the chapter's page images
        :return: The list of page images, in the correct order
        """
        if len(self._pages) == 0:
            self._pages = self._page_load_callback(self.url)
        return self._pages

    def download(
            self,
            file_path_override: Optional[str] = None,
            format_override: Optional[str] = None
    ) -> str:
        """
        Downloads the chapter to a local file or directory
        :param file_path_override: Overrides the automatically generated
                                   destination file path
        :param format_override: Overrides the class-wide format
        :return: The path to the downloaded chapter file/directory
        """
        _format = self.format if format_override is None else format_override

        tempdir = os.path.join("/tmp", self.name)
        makedirs(tempdir, delete_before=True)

        dest_path = os.path.join(self.destination_dir, self.name)
        if file_path_override:
            dest_path = file_path_override
        if not dest_path.endswith("." + _format) and _format != "dir":
            dest_path += "." + _format

        makedirs(os.path.dirname(dest_path))

        index_fill = len(str(len(self.pages)))
        downloaded = []
        for i, image in enumerate(self.pages):
            pass  # TODO download image into tempdir, append to downloaded

        if _format in ["cbz", "zip"]:
            Popen(["zip", "-j", dest_path] + downloaded).wait()
            shutil.rmtree(tempdir)
        elif _format == "dir":
            os.rename(tempdir, dest_path)
        else:
            self.logger.warning("Invalid format {}".format(_format))

        return dest_path
