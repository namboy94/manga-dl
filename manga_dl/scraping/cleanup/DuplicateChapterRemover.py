import itertools
import logging
from copy import deepcopy
from typing import List

from manga_dl.model.MangaChapter import MangaChapter
from manga_dl.model.MangaSeries import MangaSeries
from manga_dl.model.MangaVolume import MangaVolume


class DuplicateChapterRemover:
    logger = logging.getLogger("DuplicateChapterRemover")

    def remove_duplicate_chapters(self, _series: MangaSeries) -> MangaSeries:

        series = deepcopy(_series)

        for volume in series.volumes:
            self._remove_duplicates_for_volume(volume)

        return series

    def _remove_duplicates_for_volume(self, volume: MangaVolume):
        chapters: List[MangaChapter] = []
        volume_chapters = list(sorted(volume.chapters, key=lambda x: x.number))
        grouped_by_chapter = itertools.groupby(volume_chapters, lambda x: x.number)

        for _, _grouped_chapters in grouped_by_chapter:
            grouped_chapters = list(_grouped_chapters)
            selected = max(grouped_chapters, key=lambda x: x.published_at)
            chapters.append(selected)

            if len(grouped_chapters) > 1:
                self.logger.debug(f"Removed duplicates for chapter: {selected.number}")

        volume.chapters = chapters
