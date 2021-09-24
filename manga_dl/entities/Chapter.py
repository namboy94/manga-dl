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
import time
import shutil
import logging
import random
from puffotter.os import makedirs
from puffotter.print import pprint
from typing import Callable, List, Dict, Any
from typing import Optional
from subprocess import Popen, DEVNULL
from manga_dl.util.requests import download_image


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
            page_load_callback: Callable[['Chapter', str], List[str]],
            title: Optional[str] = None,
            group: Optional[str] = None,
            extras: Optional[Dict[str, Any]] = None,
            children: Optional[List["Chapter"]] = None
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
        :param title: The title of the chapter
        :param group: The group that scanlated this chapter
        :param page_load_callback: The callback used for downloading
        :param extras: Any additional information that may be needed
        :param children: Any child chapters
        """
        self.logger = logging.getLogger(self.__class__.__name__)
        self.url = url
        self.language = language
        self.series_name = series_name
        self.chapter_number = chapter_number
        self.destination_dir = destination_dir
        self.format = _format
        self._page_load_callback = page_load_callback
        self._pages = []  # type: List[str]
        self._page_load_chapters = []
        self.group = group
        self.title = title
        self.extras = extras
        self.children = children if children is not None else []

        if self.chapter_number == "" or chapter_number == "0":
            self.chapter_number = "0.0"

    @property
    def name(self) -> str:
        """
        :return: The name of the chapter
        """
        name = "{} - Chapter {}".format(self.series_name, self.chapter_number)
        if self.title is not None and self.title != "":
            name += " - " + self.title
        if self.group is not None and self.group != "":
            name += " ({})".format(self.group)
        return name

    @property
    def pages(self) -> List[str]:
        """
        Lazy-loads the URLs of the chapter's page images
        :return: The list of page images, in the correct order
        """
        to_load = [self] + self.children
        if len(to_load) == len(self._page_load_chapters):
            return self._pages
        else:
            self._page_load_chapters = to_load
            self._pages = []
            for chapter in to_load:
                self._pages += chapter._page_load_callback(
                    chapter, chapter.url
                )
        return self._pages

    @property
    def macro_chapter(self) -> int:
        """
        Calculates the 'macro' chapter number. For example:
            12 -> 12
            15.5 -> 15
            EX4 -> 4
        :return: The macro chapter number
        """
        macro = self.chapter_number.split(".")[0]
        macro_num = ""
        for char in macro:
            if char.isnumeric():
                macro_num += char
        return int(macro_num)

    @property
    def micro_chapter(self) -> int:
        """
        Calculates the 'micro' chapter number. For example:
            12 -> 0
            15.5 -> 5
            EX4 -> 0
        :return: The micro chapter number
        """
        try:
            micro = self.chapter_number.split(".")[1]
            micro_num = ""
            for char in micro:
                if char.isnumeric():
                    micro_num += char
            return int(micro_num)
        except IndexError:
            return 0

    @property
    def is_special(self) -> bool:
        """
        :return: Whether or not this is a 'special' chapter (Omake etc)
        """
        if "." in self.chapter_number or self.macro_chapter == 0:
            return True
        else:
            try:
                int(self.chapter_number)
                return False
            except ValueError:
                return True

    def add_child_chapter(self, child: "Chapter"):
        """
        Adds a child chapter.
        Useful for multi-part chapters
        :param child: The chapter to add as a child chapter
        :return: None
        """
        self.children.append(child)

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

        tempdir = os.path.join("/tmp", self.name[0:30])
        makedirs(tempdir, delete_before=True)

        dest_path = os.path.join(self.destination_dir, self.name)
        if file_path_override:
            dest_path = file_path_override
        if not dest_path.endswith("." + _format) and _format != "dir":
            dest_path += "." + _format

        makedirs(os.path.dirname(dest_path))

        index_fill = len(str(len(self.pages)))
        downloaded = []

        for i, image_url in enumerate(self.pages):

            cloudflare = False
            if image_url.startswith("CF!"):
                image_url = image_url[3:]
                cloudflare = True

            ext = image_url.rsplit(".", 1)[1]
            filename = "{}.{}".format(str(i).zfill(index_fill), ext)
            image_file = os.path.join(tempdir, filename)

            pprint("{} Chapter {} ({}/{})".format(
                self.series_name,
                self.chapter_number,
                i + 1,
                len(self.pages)
            ), fg="black", bg="lyellow", end="\r")

            download_image(image_url, image_file, use_cfscrape=cloudflare)
            downloaded.append(image_file)
            time.sleep(random.randint(1, 2))

        if len(downloaded) == 0:
            self.logger.warning("Couldn't download chapter {}".format(self))
        else:
            if _format in ["cbz", "zip"]:
                self.logger.debug("Zipping Files")
                Popen(["zip", "-j", dest_path] + downloaded,
                      stdout=DEVNULL, stderr=DEVNULL).wait()
                shutil.rmtree(tempdir)
            elif _format == "dir":
                os.rename(tempdir, dest_path)
            else:
                self.logger.warning("Invalid format {}".format(_format))

        return dest_path

    def __str__(self) -> str:
        """
        :return: The string representation of the object
        """
        return self.name

    def __eq__(self, other: object) -> bool:
        """
        Checks for equality with other objects
        :param other: The other object
        :return: Whether or not the objects are  the same
        """
        if not isinstance(other, Chapter):
            return False
        else:
            return other.url == self.url
