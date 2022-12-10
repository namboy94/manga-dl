from collections.abc import Set
from enum import Enum


# Define the Enum class
class MangaFileFormat(Enum):
    CBZ = "cbz"
    ZIP = "zip"
    DIR = "dir"

    @staticmethod
    def options() -> Set[str]:
        return {x.value for x in MangaFileFormat}
