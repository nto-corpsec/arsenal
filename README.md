# arsenal

Инструменты команды: один Python-пакет, ролевые модули, общий CI.

## Зачем

Каждая роль пишет свои скрипты, но инфраструктура (линтеры, тесты, security-гейты,
хеширование артефактов) — общая. Это снимает дублирование и не даёт ролям разъехаться
по стилю и качеству.

## Структура

```
src/nto/
├── cli.py                 # nto hash | manifest | scan-flags | redact | timebox
├── common/
│   ├── artifacts.py       # SHA-256, манифесты, chain of custody
│   ├── flags.py           # поиск и маскирование флагов
│   └── timebox.py         # таймбоксы 25/5
└── roles/
    ├── soceng/handles.py  # варианты ников для OSINT
    ├── dfir/timeline.py   # слияние событий в таймлайн
    ├── netsec/nmap.py     # разбор nmap XML
    ├── websec/encoding.py # кодирование пейлоадов
    └── osint/domains.py   # нормализация хостов, eTLD+1
```

## Быстрый старт

```bash
uv sync                 # окружение
uv run nto hash file    # SHA-256
uv run nto scan-flags . # поиск флагов
uv run pytest --cov=src # тесты
make check              # всё сразу
```

## Владение

| Путь | Владелец |
|---|---|
| `src/nto/common/`, `src/nto/cli.py` | TeamLead |
| `src/nto/roles/soceng/` | Social Engineering |
| `src/nto/roles/dfir/` | DFIR |
| `src/nto/roles/netsec/` | Network Security |
| `src/nto/roles/websec/` | Web Security |
| `src/nto/roles/osint/` | OSINT & Analytics |

## Гейты CI

| Проверка | Что делает |
|---|---|
| `ruff format` / `ruff check` | стиль и ошибки |
| `mypy` | типы |
| `pytest --cov` | тесты, порог покрытия 70% |
| `bandit` | типовые уязвимости Python |
| `semgrep p/python` | SAST |
| `gitleaks` | секреты в истории |
| `no-leak` | флаги и ключи в публичном коде |
| `codeql` | глубокий анализ (push в main, weekly) |

## Правила

- Новый инструмент — модуль роли + тест + запись в README.
- Никаких сетевых вызовов в тестах: фикстуры, моки, записанные ответы.
- Флаги и реальные ответы в репозиторий не попадают никогда.
