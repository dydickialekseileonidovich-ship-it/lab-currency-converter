import pytest
from main import work_session, short_break, long_break


def test_work_session_default_and_custom():
    assert work_session() == 25
    assert work_session(30) == 30


def test_work_session_invalid():
    with pytest.raises(ValueError, match="minutes must be > 0"):
        work_session(0)
    with pytest.raises(ValueError, match="minutes must be > 0"):
        work_session(-5)


def test_short_break_default_and_custom():
    assert short_break() == 5
    assert short_break(10) == 10


def test_short_break_invalid():
    with pytest.raises(ValueError, match="minutes must be > 0"):
        short_break(0)


def test_long_break_logic():
    # 1, 2, 3 -> короткий перерыв (5 мин)
    assert long_break(cycle=1, every=4, minutes=15) == 5
    assert long_break(cycle=2, every=4, minutes=15) == 5
    assert long_break(cycle=3, every=4, minutes=15) == 5

    # 4 -> длинный перерыв (15 мин)
    assert long_break(cycle=4, every=4, minutes=15) == 15

    # 5, 6, 7 -> короткий; 8 -> длинный
    assert long_break(cycle=5, every=4, minutes=15) == 5
    assert long_break(cycle=8, every=4, minutes=15) == 15


def test_long_break_invalid():
    with pytest.raises(ValueError):
        long_break(cycle=0)
    with pytest.raises(ValueError):
        long_break(cycle=1, every=0)
    with pytest.raises(ValueError):
        long_break(cycle=1, minutes=0)
