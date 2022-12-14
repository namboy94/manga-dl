import logging
from copy import deepcopy
from decimal import Decimal
from typing import List, Optional

from manga_dl.model.MangaChapter import MangaChapter
from manga_dl.model.MangaSeries import MangaSeries
from manga_dl.model.MangaVolume import MangaVolume


class ChapterNormalizer:
    logger = logging.getLogger("ChapterNormalizer")

    def normalize_chapters(self, _series: MangaSeries):

        series = deepcopy(_series)
        volumes = self._order_volumes(series)

        gaps: List[Decimal] = []

        for i in range(1, len(volumes)):
            volume = volumes[i]
            previous_volume = volumes[i - 1]

            gaps += self._find_gaps(previous_volume, volume)
            self._adjust_chapter_numbers(volume, previous_volume, gaps)

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

    def _adjust_chapter_numbers(self, volume: MangaVolume, previous_volume: MangaVolume, gaps: List[Decimal]):
        if len(previous_volume.chapters) == 0:
            return

        last_chapter = list(sorted(previous_volume.chapters, key=lambda x: x.number))[0]
        chapters = list(sorted(volume.chapters, key=lambda x: x.number))

        gap_fillers = [chapter for chapter in chapters if chapter.number in gaps]
        above_gap = [] if len(gaps) == 0 else [chapter for chapter in chapters if chapter.number > max(gaps)]
        to_check = [chapter for chapter in chapters if chapter not in gap_fillers + above_gap]

        if len(to_check) == 0 or to_check[0].number > last_chapter.number:
            return

        for i, chapter in enumerate(to_check):
            previous_chapter = None if i == 0 else to_check[i - 1]
            self._adjust_chapter_number(chapter, previous_chapter, last_chapter, i, len(to_check) != len(chapters))

    def _adjust_chapter_number(
            self,
            chapter: MangaChapter,
            previous_chapter: Optional[MangaChapter],
            previous_volume_last_chapter: MangaChapter,
            index: int,
            has_gap: bool
    ):

        if has_gap:
            last_chapter_macro = previous_volume_last_chapter.get_macro_micro_chapter()[0]
            chapter_number = Decimal("0.5") + Decimal("0.01") * (index + 1) + last_chapter_macro
        else:
            chapter_number = self._calculate_chapter_number(chapter, previous_chapter, previous_volume_last_chapter)

        if chapter_number != chapter.number:
            self.logger.debug(f"Normalizing "
                              f"vol. {chapter.volume} "
                              f"chapter {chapter.number} to "
                              f"Ch. {chapter_number}")
            chapter.number = chapter_number

    @staticmethod
    def _calculate_chapter_number(
            chapter: MangaChapter,
            previous_chapter: Optional[MangaChapter],
            previous_volume_last_chapter: MangaChapter
    ) -> Decimal:
        last_chapter_number = previous_volume_last_chapter.get_macro_micro_chapter()[0]
        adjusted_chapter_number = chapter.number + last_chapter_number
        previous_chapter_number = adjusted_chapter_number if previous_chapter is None else previous_chapter.number

        if previous_chapter_number < chapter.number:
            return chapter.number

        return min(adjusted_chapter_number, previous_chapter_number + 1)

    def _find_gaps(self, volume: MangaVolume, next_volume: MangaVolume) -> List[Decimal]:
        full_chapter_numbers = self._find_full_chapters(volume)
        next_full_chapter_numbers = self._find_full_chapters(next_volume)

        if len(full_chapter_numbers) == 0 or len(next_full_chapter_numbers) == 0:
            return []

        first = full_chapter_numbers[0]
        last = next_full_chapter_numbers[0]

        return [
            Decimal(chapter_number)
            for chapter_number in range(first, last)
            if chapter_number not in full_chapter_numbers
        ]

    @staticmethod
    def _find_full_chapters(vol: MangaVolume) -> List[int]:
        return [
            chapter.get_macro_micro_chapter()[0]
            for chapter in vol.chapters
            if chapter.get_macro_micro_chapter()[1] == 0
        ]
