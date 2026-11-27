import pytest
from src.password_checker import evaluate_password_strength


def test_empty_and_short_password():
    res = evaluate_password_strength("")
    assert res["score"] == 0
    assert res["level"] == "Очень слабый"
    assert res["is_acceptable"] is False
    assert len(res["feedback"]) == 4

    res2 = evaluate_password_strength("abc")
    assert res2["score"] == 0
    assert "Увеличьте длину пароля минимум до 8 символов." in res2["feedback"]


def test_medium_password():
    res = evaluate_password_strength("Password123")
    # Длина >= 8 (1) + Заглавные и строчные (1) + Цифры (1) = 3
    assert res["score"] == 3
    assert res["level"] == "Хороший"
    assert res["is_acceptable"] is True
    assert any("специальный символ" in f for f in res["feedback"])


def test_strong_password():
    res = evaluate_password_strength("MySuper$ecretP@ss2026")
    # >= 8 (1), >= 12 (1), регистры (1), цифры (1), спецсимволы (1) = 5
    assert res["score"] == 5
    assert res["level"] == "Очень надёжный"
    assert res["is_acceptable"] is True
    assert res["feedback"] == []


def test_invalid_type():
    with pytest.raises(TypeError):
        evaluate_password_strength(None)  # type: ignore
