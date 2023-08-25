from datetime import datetime, date, time


def convert_datetime(s: bytes) -> datetime:
    return datetime.strptime(s.decode(encoding="utf-8"), "%Y-%m-%d %H:%M:%S")


def convert_date(s: bytes) -> date:
    return date.fromisoformat(s.decode(encoding="utf-8"))


def convert_time(s: bytes) -> time:
    return time.fromisoformat(s.decode(encoding="utf-8"))
