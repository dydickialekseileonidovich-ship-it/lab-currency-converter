# Лабораторная работа №8: Документация проекта — Markdown и Swagger (OpenAPI)
**Студент:** Дудицкий А. Л.  
**Вариант:** 10  
**Тема:** Портал стипендиальных заявок

> **Постановка задачи (Вариант 10):** Портал стипендиальных заявок. Подача и статус заявки. User: подать, отследить статус. Tech: статусы и роли (студент/сотрудник). OpenAPI: создать заявку, статус, список своих заявок, смена статуса (admin).

---

## 1. Состав документации
- [Руководство пользователя](docs/user.md) — сценарии подачи и отслеживания заявок для студентов и сотрудников деканата, FAQ.
- [Техническая документация](docs/tech.md) — архитектура, структура, ролевая модель (RBAC), матрица состояний и переменные окружения.
- OpenAPI: [openapi.yaml](openapi.yaml) — спецификация OpenAPI 3.0.3 (4 операции: `POST /applications`, `GET /applications`, `GET /applications/{id}`, `PATCH /applications/{id}/status`).

## 2. Как просмотреть спецификацию OpenAPI / Swagger
- Откройте веб-редактор [Swagger Editor](https://editor.swagger.io/) и импортируйте файл `openapi.yaml`.
- Или запустите локальный контейнер Swagger UI:
```bash
docker run -p 8081:8080 -e SWAGGER_JSON=/spec/openapi.yaml -v "$(pwd)/openapi.yaml:/spec/openapi.yaml" swaggerapi/swagger-ui
```
Интерфейс будет доступен по адресу `http://localhost:8081`.
