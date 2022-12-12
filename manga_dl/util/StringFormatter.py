from manga_dl.model.MangaChapter import MangaChapter
from manga_dl.model.MangaSeries import MangaSeries
from manga_dl.model.MangaVolume import MangaVolume


class StringFormatter:

    def format_series(self, series: MangaSeries) -> str:

        series_string = f"[{series.id}]{series.name} (author={series.author}, artist={series.artist})"
        for volume in series.volumes:
            volume_string = self.format_volume(volume).replace("\n  ", "\n    ")
            series_string += f"\n  {volume_string}"

        return series_string

    def format_volume(self, volume: MangaVolume) -> str:

        volume_string = "No Volume" if volume.volume_number is None else f"Vol. {volume.volume_number}"
        for chapter in volume.chapters:
            volume_string += f"\n  {self.format_chapter(chapter)}"

        return volume_string

    # noinspection PyMethodMayBeStatic
    def format_chapter(self, chapter: MangaChapter) -> str:
        title = "Untitled" if chapter.title == "" else chapter.title
        return f"Ch. {chapter.number} - {title}"
