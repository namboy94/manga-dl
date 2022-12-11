from pathlib import Path
from typing import List

from manga_dl.bundling.MangaBundler import MangaBundler
from manga_dl.model.DownloadedFile import DownloadedFile
from manga_dl.model.MangaChapter import MangaChapter
from manga_dl.model.MangaFileFormat import MangaFileFormat
from manga_dl.model.MangaSeries import MangaSeries


class DirectoryBundler(MangaBundler):

    def get_file_format(self) -> MangaFileFormat:
        return MangaFileFormat.DIR

    def bundle(self, images: List[DownloadedFile], destination: Path, series: MangaSeries, chapter: MangaChapter):
        destination.mkdir(parents=True, exist_ok=True)
        for image in images:
            with open(destination / image.filename, "wb") as imagefile:
                imagefile.write(image.data)
