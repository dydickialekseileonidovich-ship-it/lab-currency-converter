# main.py

def work_session(minutes: int = 25) -> int:
    """Возвращает длительность рабочей сессии в минутах."""
    if minutes <= 0:
        raise ValueError("minutes must be > 0")
    return minutes


def short_break(minutes: int = 5) -> int:
    """Возвращает длительность короткого перерыва в минутах."""
    if minutes <= 0:
        raise ValueError("minutes must be > 0")
    return minutes


def long_break(cycle: int, every: int = 4, minutes: int = 15) -> int:
    """
    Каждый every-й цикл — long break, иначе short (5).
    cycle начинается с 1.
    """
    if cycle <= 0:
        raise ValueError("cycle must be >= 1")
    if every <= 0:
        raise ValueError("every must be > 0")
    if minutes <= 0:
        raise ValueError("minutes must be > 0")

    if cycle % every == 0:
        return minutes
    return short_break(5)
