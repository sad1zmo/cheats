from datacenter.models import Schoolkid
from datacenter.models import Mark
from datacenter.models import Chastisement
from datacenter.models import Lesson
from datacenter.models import Commendation
import random


COMMENDATION_TEXTS = ['Молодец!', 'Отлично!', 'Хорошо!',
                      'Гораздо лучше, чем я ожидал!',
                      'Ты меня приятно удивил!',
                      'Великолепно!', 'Прекрасно!',
                      'Ты меня очень обрадовал!',
                      'Именно этого я давно ждал от тебя!',
                      'Сказано здорово – просто и ясно!',
                      'Ты, как всегда, точен!',
                      'Очень хороший ответ!', 'Талантливо!',
                      'Ты сегодня прыгнул выше головы!',
                      'Я поражен!', 'Я тобой горжусь!',
                      'Уже существенно лучше!', 'Потрясающе!',
                      'Прекрасное начало!', 'Так держать!',
                      'Ты на верном пути!', 'Здорово!',
                      'Это как раз то, что нужно!',
                      'С каждым разом у тебя получается всё лучше!',
                      'Мы с тобой не зря поработали!',
                      'Я вижу, как ты стараешься!',
                      'Ты растешь над собой!',
                      'Ты многое сделал, я это вижу!',
                      'Теперь у тебя точно все получится!']


def fix_marks(schoolkid_name):
    schoolkid_name = handle_schoolkid_exceptions(schoolkid_name)
    if schoolkid_name:
        update_marks = Mark.objects.filter(
            schoolkid=schoolkid_name, points__lt=4).update(points=5)
        return update_marks


def delete_chastisements(schoolkid_name):
    schoolkid_name = handle_schoolkid_exceptions(schoolkid_name)
    if schoolkid_name:
        chastisements = Chastisement.objects.filter(schoolkid=schoolkid_name)
        chastisements.delete()


def create_commendation(schoolkid_name, subject_title):
    schoolkid = handle_schoolkid_exceptions(schoolkid_name)
    if schoolkid:
        lesson = Lesson.objects.filter(
            subject__title=subject_title,
            year_of_study=schoolkid.year_of_study,
            group_letter=schoolkid.group_letter)
        if lesson.first():
            lesson_date = lesson.last().date
            teacher = lesson.first().teacher
            commendation = Commendation.objects.create(
                text=random.choice(COMMENDATION_TEXTS),
                created=lesson_date,
                schoolkid=schoolkid,
                subject=lesson.first().subject,
                teacher=teacher)
            return commendation
        else:
            print(f"Предмет с названием '{subject_title}' не найден")


def handle_schoolkid_exceptions(schoolkid_name):
    try:
        schoolkid_name = Schoolkid.objects.get(
            full_name__contains=schoolkid_name)
        return schoolkid_name
    except Schoolkid.MultipleObjectsReturned:
        print(f"Найдено более одного ученика по имени {schoolkid_name}, "
              f"Укажите ФИО")
    except Schoolkid.DoesNotExist:
        print(f"Ученик с именем {schoolkid_name} не найден")
