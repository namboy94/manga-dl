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


import zipfile
import os


def create_cbz(directory, output_file):
    images = [f for f in os.listdir(directory) if os.path.splitext(f)[1].lower() in [".jpg", ".png"]]

    with zipfile.ZipFile(output_file, "w") as cbz:
        for image in images:
            cbz.write(os.path.join(directory, image), arcname=image)
