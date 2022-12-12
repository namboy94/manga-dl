import itertools
import logging
from copy import deepcopy
from decimal import Decimal
from typing import List

from manga_dl.model.MangaChapter import MangaChapter
from manga_dl.model.MangaSeries import MangaSeries
from manga_dl.model.MangaVolume import MangaVolume


class MultipartChapterMerger:
    logger = logging.getLogger("MultipartChapterMerger")

    def merge_multipart_chapters(self, _series: MangaSeries) -> MangaSeries:
        series = deepcopy(_series)

        for volume in series.volumes:
            self._merge_for_volume(volume)

        return series

    def _merge_for_volume(self, volume: MangaVolume):
        chapters: List[MangaChapter] = []
        volume_chapters = list(sorted(volume.chapters, key=lambda x: x.number))
        grouped_by_macro_chapter = itertools.groupby(volume_chapters, lambda x: x.get_macro_micro_chapter()[0])

        for macro_chapter, _grouped_chapters in grouped_by_macro_chapter:
            grouped_chapters = list(sorted(_grouped_chapters, key=lambda x: x.number))

            to_merge = [grouped_chapters.pop(0)]

            while len(grouped_chapters) > 0 and grouped_chapters[0].number - to_merge[-1].number <= Decimal("0.1"):
                to_merge.append(grouped_chapters.pop(0))

            merged_chapter = self._merge_chapters(to_merge)
            chapters += [merged_chapter] + grouped_chapters

        volume.chapters = chapters

    def _merge_chapters(self, chapters: List[MangaChapter]) -> MangaChapter:

        if len(chapters) == 1:
            return chapters[0]

        self.logger.debug(f"Merging chapters {list(map(lambda x: x.number, chapters))}")

        latest_published_at = max(chapters, key=lambda x: x.published_at).published_at
        merged = chapters.pop(0)

        if merged.number % 1 == Decimal(0):
            return self._handle_duplicate(merged, chapters)

        merged.published_at = latest_published_at
        merged.number = Decimal(merged.get_macro_micro_chapter()[0])

        for chapter in chapters:
            merged.pages += chapter.pages

        return merged

    def _handle_duplicate(self, single: MangaChapter, rest: List[MangaChapter]) -> MangaChapter:
        rest_merged = self._merge_chapters(rest)

        candidates = [single, rest_merged]

        if len(single.pages) != len(rest_merged.pages):
            return max(candidates, key=lambda x: len(x.pages))

        return max(candidates, key=lambda x: x.published_at)
