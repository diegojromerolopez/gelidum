import datetime


def utcnow() -> datetime.datetime:
    try:
        return datetime.datetime.now(datetime.UTC)
    except AttributeError:  # pragma: no cover
        return datetime.datetime.utcnow()  # pragma: no cover
