# Техническая документация: Портал стипендиальных заявок

## 1. Архитектура решения
Система построена по сервисной REST-архитектуре:
- **Presentation Layer:** Веб-клиент (SPA) и OpenAPI / Swagger UI для взаимодействия с API.
- **Backend / API:** Python-сервис бизнес-логики (REST API v1, базовый путь `/api/v1`).
- **Data Persistence:** Реляционная СУБД PostgreSQL для хранения заявок и аудита переходов статусов.
- **Object Storage:** Хранилище MinIO/S3 для сканов справок, дипломов и подтверждающих документов.

## 2. Структура документации и спецификации
```text
Lab_8_Docs_Markdown_Swagger/
├── README.md        # Обзор проекта, постановка задачи и навигация
├── docs/
│   ├── user.md      # Пользовательское руководство (сценарии и FAQ)
│   └── tech.md      # Техническая документация (архитектура, RBAC, конфиг)
└── openapi.yaml     # Формальная спецификация API в формате OpenAPI 3.0.3
```

## 3. Ролевая модель (RBAC)
- **STUDENT (Студент):**
  - Разрешено: создание заявки (`POST /applications`), просмотр исключительно собственных заявок (`GET /applications?student_card={id}`), просмотр карточки своей заявки (`GET /applications/{id}`).
  - Запрещено: просмотр чужих заявок, изменение статуса рассмотрения (`PATCH /applications/{id}/status`).
- **DEANERY_STAFF / ADMIN (Сотрудник деканата / администратор):**
  - Разрешено: просмотр всех заявок факультета с фильтрацией по статусу, перевод заявки в статусы `IN_REVIEW`, `NEEDS_INFO`, `APPROVED`, `REJECTED` с комментарием.
- **ACCOUNTANT (Бухгалтерия):**
  - Разрешено: выгрузка утверждённых заявок (`status=APPROVED`) в платёжный реестр.

## 4. Матрица допустимых состояний заявки
```text
[DRAFT] ---> [SUBMITTED] ---> [IN_REVIEW] ---> [APPROVED]
                                   |      \---> [REJECTED]
                                   v
                             [NEEDS_INFO] ---> [IN_REVIEW]
                                   \---------> [REJECTED]
```

## 5. Конфигурация и запуск просмотра OpenAPI
Переменные окружения бэкенд-сервиса (согласованы с ЛР №7):
- `DB_HOST`, `DB_PORT`, `DB_NAME`, `DB_USER`, `DB_PASSWORD` — параметры подключения к PostgreSQL;
- `API_EXTERNAL_PORT` (по умолчанию `8080`) — внешний HTTP-порт API.

Локальный просмотр спецификации в Swagger UI:
```bash
docker run -p 8081:8080 -e SWAGGER_JSON=/spec/openapi.yaml -v "$(pwd)/openapi.yaml:/spec/openapi.yaml" swaggerapi/swagger-ui
```
