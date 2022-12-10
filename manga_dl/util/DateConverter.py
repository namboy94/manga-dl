from datetime import datetime


class DateConverter:

    @staticmethod
    def convert_to_string(date: datetime) -> str:
        return date.strftime("%Y-%m-%dT%H:%M:%S")

    @staticmethod
    def convert_to_datetime(date_string: str) -> datetime:
        return datetime.strptime(date_string.split("+")[0], "%Y-%m-%dT%H:%M:%S")
