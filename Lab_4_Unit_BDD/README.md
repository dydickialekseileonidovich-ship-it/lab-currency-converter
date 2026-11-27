# Лабораторная работа №4: Юнит-тесты и BDD-сценарии
**Студент:** Дудицкий А. Л.  
**Вариант:** 10  
**Тема:** Таймер помодоро (минуты)

---

## 1. Описание задачи
Реализовать функции расчёта интервалов для таймера Pomodoro:
- `work_session(minutes=25)`
- `short_break(minutes=5)`
- `long_break(cycle, every=4, minutes=15)` — где каждый 4-й цикл перерыв равен 15 минутам, а в промежуточные (1, 2, 3, 5...) — 5 минутам.

---

## 2. Цикл разработки: Red → Green → Refactor

### Фаза RED (Красный)
1. Написаны пустые сигнатуры функций (stubs с `...` или `pass`).
2. Написаны юнит-тесты `test_unit.py` и BDD-сценарий `features/pomodoro_breaks.feature`.
3. Запуск `pytest` завершился падением: тесты упали с `AssertionError / TypeError` из-за возврата `None`.

### Фаза GREEN (Зелёный)
1. Написана минимально необходимая реализация:
   ```python
   def short_break(minutes: int = 5) -> int:
       return minutes

   def long_break(cycle: int, every: int = 4, minutes: int = 15) -> int:
       if cycle % every == 0:
           return minutes
       return 5
   ```
2. Все тесты успешно прошли.

### Фаза REFACTOR (Рефакторинг)
1. Добавлена строгая валидация краевых значений (`cycle <= 0`, `every <= 0`, `minutes <= 0`).
2. Захардкоженный возврат `5` заменён на вызов `short_break(5)` для соблюдения DRY.
3. Добавлены docstrings и аннотации типов `typing`. Все тесты повторно запущены и остались зелёными.

---

## 3. Инструкция по запуску

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Запуск юнит-тестов
pytest test_unit.py -v

# Запуск BDD-сценариев
pytest test_bdd.py -v
```
