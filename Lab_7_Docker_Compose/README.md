# Лабораторная работа №7: Docker и Docker Compose
**Студент:** Дудицкий А. Л.  
**Вариант:** 10  
**Тема:** Портал стипендиальных заявок (API + PostgreSQL)

---

## 1. Структура проекта
- `api` (Python / Flask) — REST API для подачи и управления стипендиями.
- `db` (PostgreSQL 15 Alpine) — реляционная СУБД.
- `compose.yaml` — декларативная конфигурация мультиконтейнерного развёртывания.

## 2. Сетевая адресация и порты
| Сервис | Порт внутри сети Docker | Внешний порт на хосте | Назначение |
|---|---|---|---|
| `api` | `5000` | `8080` | HTTP REST API эндпоинты |
| `db` | `5432` | `5433` | Доступ к СУБД для администрирования |

---

## 3. Инструкция по сборке и запуску

### Запуск контейнеров
```bash
docker compose up --build -d
```

### Проверка работоспособности (Healthcheck)
```bash
curl http://localhost:8080/health
# Ответ: {"database":"connected","status":"healthy"}
```

### Примеры запросов к API

1. **Подать заявку на стипендию:**
```bash
curl -X POST http://localhost:8080/applications \
     -H "Content-Type: application/json" \
     -d '{"student_name": "Дудицкий А.Л.", "student_card": "СТ-102938", "scholarship_type": "ACADEMIC"}'
```

2. **Сменить статус заявки (например, на APPROVED):**
```bash
curl -X PATCH http://localhost:8080/applications/1/status \
     -H "Content-Type: application/json" \
     -d '{"status": "APPROVED"}'
```

3. **Получить список заявок по статусу:**
```bash
curl "http://localhost:8080/applications?status=APPROVED"
```

### Остановка
```bash
docker compose down -v
```
