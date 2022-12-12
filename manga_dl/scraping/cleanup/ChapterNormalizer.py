from copy import deepcopy
from decimal import Decimal
from typing import List, Optional

from manga_dl.model.MangaChapter import MangaChapter
from manga_dl.model.MangaSeries import MangaSeries
from manga_dl.model.MangaVolume import MangaVolume


class ChapterNormalizer:

    def normalize_chapters(self, _series: MangaSeries):

        series = deepcopy(_series)
        volumes = self._order_volumes(series)

        for i in range(1, len(volumes)):
            volume = volumes[i]
            previous_volume = volumes[i - 1]
            self._adjust_chapter_numbers(volume, previous_volume)

        return series

    @staticmethod
    def _order_volumes(series: MangaSeries) -> List[MangaVolume]:
        if len(series.volumes) == 0:
            return []

        volumes = series.volumes
        volumes.sort(key=lambda x: Decimal(0) if x.volume_number is None else x.volume_number)

        if volumes[0].volume_number is None:
            volumes.append(volumes.pop(0))

        return volumes

    def _adjust_chapter_numbers(self, volume: MangaVolume, previous_volume: MangaVolume):
        if len(previous_volume.chapters) == 0:
            return

        last_chapter = list(sorted(previous_volume.chapters, key=lambda x: x.number))[0]
        chapters = sorted(volume.chapters, key=lambda x: x.number)

        if chapters[0].number <= last_chapter.number:
            for i, chapter in enumerate(chapters):
                previous_chapter = None if i == 0 else chapters[i - 1]
                chapter.number = self._calculate_chapter_number(chapter, previous_chapter, last_chapter)

    @staticmethod
    def _calculate_chapter_number(
            chapter: MangaChapter,
            previous_chapter: Optional[MangaChapter],
            previous_volume_last_chapter: MangaChapter
    ) -> Decimal:
        adjusted_chapter_number = chapter.number + previous_volume_last_chapter.number
        previous_chapter_number = adjusted_chapter_number if previous_chapter is None else previous_chapter.number

        if previous_chapter_number < chapter.number:
            return chapter.number

        return min(adjusted_chapter_number, previous_chapter_number + 1)
