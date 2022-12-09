from pathlib import Path
from typing import List

from manga_dl.neo.bundling.MangaBundler import MangaBundler
from manga_dl.neo.model.DownloadedFile import DownloadedFile
from manga_dl.neo.model.MangaChapter import MangaChapter
from manga_dl.neo.model.MangaFileFormat import MangaFileFormat
from manga_dl.neo.model.MangaSeries import MangaSeries


class DirectoryBundler(MangaBundler):

    def get_file_format(self) -> MangaFileFormat:
        return MangaFileFormat.DIR

    def bundle(self, images: List[DownloadedFile], destination: Path, series: MangaSeries, chapter: MangaChapter):
        series_dir = destination.parent / destination.name.rsplit(".", 1)[0]
        series_dir.mkdir(parents=True, exist_ok=True)
        for image in images:
            with open(series_dir / image.filename, "wb") as imagefile:
                imagefile.write(image.data)
