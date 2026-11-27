# Лабораторная работа №6: Настройка простого пайплайна CI/CD
**Студент:** Дудицкий А. Л.  
**Вариант:** 10  
**Тема:** Проверка сложности пароля (score)

[![CI/CD Password Strength Pipeline](https://github.com/dydickialekseileonidovich-ship-it/lab-currency-converter/actions/workflows/ci.yml/badge.svg)](https://github.com/dydickialekseileonidovich-ship-it/lab-currency-converter/actions/workflows/ci.yml)

> **Постановка задачи (Вариант 10):** Проверка сложности пароля (score). Модуль оценки силы пароля и текстовых рекомендаций. Тесты шкал. Пайплайн test + deploy документации на Pages.

---

## 1. Архитектура проекта
- `src/password_checker.py`: Модуль скоринга сложности пароля.
- `tests/test_password_checker.py`: Unit-тесты граничных условий и шкал.
- `requirements.txt`: Зависимости для тестирования и линтинга (`pytest`, `pytest-cov`, `flake8`).
- `../.github/workflows/ci.yml` (и локальная копия `.github/workflows/ci.yml`): Конфигурация пайплайна CI/CD GitHub Actions.
- `docs/index.md`: Пользовательская документация, публикуемая как артефакт и на GitHub Pages (`gh-pages`).

---

## 2. Устройство пайплайна CI/CD
1. **CI-стадия (Job `test`):**
   - Срабатывает на каждый `push` и `pull_request` в ветку `main`.
   - Разворачивает контейнер Ubuntu с Python 3.11.
   - Запускает статический анализ кода линтером `flake8`.
   - Запускает набор тестов `pytest` с генерацией покрытия кода. При падении хотя бы одного теста сборка прерывается.
2. **CD-стадия (Job `deploy-docs`):**
   - Срабатывает **только** при успешном прохождении тестов и **только** для коммитов в ветку `main`.
   - Собирает статический сайт документации из каталога `docs/` в каталог `public/`.
   - Публикует артефакт на GitHub Pages с помощью `peaceiris/actions-gh-pages`.

---

## 3. Локальный запуск
```bash
pip install -r requirements.txt
pytest tests/ -v
```
