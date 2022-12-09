from dataclasses import dataclass


@dataclass
class MangaPage:
    image_file: str
    page_number: int

    def get_filename(self) -> str:
        return self.image_file.split("/")[-1]
