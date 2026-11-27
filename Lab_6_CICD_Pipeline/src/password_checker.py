# src/password_checker.py
import re
from typing import Dict, List, Any


def evaluate_password_strength(password: str) -> Dict[str, Any]:
    """
    Оценивает надёжность пароля по 5-балльной шкале (0 - 5)
    и формирует список текстовых рекомендаций.
    """
    if not isinstance(password, str):
        raise TypeError("Password must be a string")

    score = 0
    feedback: List[str] = []

    if len(password) >= 8:
        score += 1
    else:
        feedback.append("Увеличьте длину пароля минимум до 8 символов.")

    if len(password) >= 12:
        score += 1

    if re.search(r"[a-z]", password) and re.search(r"[A-Z]", password):
        score += 1
    else:
        feedback.append("Используйте как заглавные, так и строчные буквы.")

    if re.search(r"\d", password):
        score += 1
    else:
        feedback.append("Добавьте хотя бы одну цифру.")

    if re.search(r"[!@#$%^&*(),.?\":{}|<>\-_=+\[\]~/`]", password):
        score += 1
    else:
        feedback.append("Добавьте хотя бы один специальный символ (например: !, @, #, $, %).")

    # Уровень надёжности
    levels = {
        0: "Очень слабый",
        1: "Слабый",
        2: "Удовлетворительный",
        3: "Хороший",
        4: "Надёжный",
        5: "Очень надёжный"
    }

    return {
        "score": score,
        "max_score": 5,
        "level": levels.get(score, "Очень слабый"),
        "feedback": feedback,
        "is_acceptable": score >= 3
    }
