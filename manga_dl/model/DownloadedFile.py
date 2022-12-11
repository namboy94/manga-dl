from dataclasses import dataclass


@dataclass
class DownloadedFile:
    data: bytes
    filename: str

    def get_extension(self) -> str:
        if "." not in self.filename:
            return ""
        return self.filename.rsplit(".")[-1]
