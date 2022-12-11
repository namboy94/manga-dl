import itertools
from copy import deepcopy
from typing import List

from manga_dl.model.MangaChapter import MangaChapter
from manga_dl.model.MangaSeries import MangaSeries
from manga_dl.model.MangaVolume import MangaVolume


class DuplicateChapterRemover:

    def remove_duplicate_chapters(self, _series: MangaSeries) -> MangaSeries:

        series = deepcopy(_series)

        for volume in series.volumes:
            self._remove_duplicates_for_volume(volume)

        return series

    @staticmethod
    def _remove_duplicates_for_volume(volume: MangaVolume):
        chapters: List[MangaChapter] = []
        volume_chapters = list(sorted(volume.chapters, key=lambda x: x.number))
        grouped_by_chapter = itertools.groupby(volume_chapters, lambda x: x.number)

        for _, grouped_chapters in grouped_by_chapter:
            selected = max(grouped_chapters, key=lambda x: x.published_at)
            chapters.append(selected)

        volume.chapters = chapters
