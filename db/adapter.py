from datetime import datetime, date, time


def adapt_datetime(dt: datetime) -> str:
    return dt.strftime("%Y-%m-%d %H:%M:%S")


def adapt_date(d: date) -> str:
    return d.strftime("%Y-%m-%d")


def adapt_time(t: time) -> str:
    return t.strftime("%H:%M:%S")
