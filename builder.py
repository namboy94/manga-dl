"""
LICENSE:
Copyright 2016 Hermann Krumrey

This file is part of manga_dl.

    manga_dl is a program that allows downloading manga files from various
    sources

    manga_dl is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    manga_dl is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with manga_dl.  If not, see <http://www.gnu.org/licenses/>.
LICENSE
"""

import manga_dl.metadata as metadata
from gitlab_build_scripts.project_builders.python import build
from gitlab_build_scripts.buildmodules.python.PyInstallerLinux import PyInstallerLinux
from gitlab_build_scripts.buildmodules.python.PyInstallerWindows import PyInstallerWindows


if __name__ == "__main__":
    build(metadata, [PyInstallerLinux, PyInstallerWindows])
