# Система управления журналом школы

## Обзор

Это приложение на Django предоставляет функционал для управления школьными данными, такими как оценки студентов, похвалы, выговоры и информация о преподавателях. Включает функции для исправления низких оценок, удаления выговоров и создания похвалы для студентов.

## Установка

### Предварительные требования

- Python 3.x
- Django 3.x
- PostgreSQL (рекомендуется для использования в продакшн)

### Шаги установки

1. Клонировать репозиторий:

   ```bash
   git clone this_repository
   ```

2. Перейти в директорию проекта:

   ```bash
   cd your_project_directory
   ```

3. Установить зависимости:

   ```bash
   pip install -r requirements.txt
   ```

4. Применить миграции базы данных:

   ```bash
   python manage.py migrate
   ```

Подразумеывается что у вас уже установлен Jango и есть база данных дневника!

## Использование

для запуска скриптов используем python shell:

```bash
python manage.py shell
```

Внутри шелла запустим:

```python
from datacenter.models import Schoolkid
from datacenter.models import Mark
from datacenter.models import Chastisement
from datacenter.models import Lesson
from datacenter.models import Commendation
from datacenter.models import Teacher
import random
from django.core.exceptions import MultipleObjectsReturned, ObjectDoesNotExist
from cheat_scripts import fix_marks, delete_chastisements, create_commendation
```

### Django Management Commands

#### Исправить Оценки

Исправляет низкие оценки для конкретного студента.

```python
fix_marks(schoolkid_name)
```

#### Удалить Выговоры

Удаляет все выговоры для конкретного студента.

```python
delete_chastisements(schoolkid_name)
```

#### Создать Похвалу

Создает похвалу для конкретного студента по указанному предмету.

```python
create_commendation(schoolkid_name, subject_title)
```
