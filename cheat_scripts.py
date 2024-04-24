from datacenter.models import Schoolkid
from datacenter.models import Mark
from datacenter.models import Chastisement
from datacenter.models import Lesson
from datacenter.models import Commendation
from datacenter.models import Teacher
import random
from django.core.exceptions import MultipleObjectsReturned, ObjectDoesNotExist


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
    try:
        schoolkid_name = Schoolkid.objects.get(
            full_name__contains=schoolkid_name)
        udate_marks = Mark.objects.filter(
            schoolkid=schoolkid_name, points__lt=4).update(points=5)
        return udate_marks
    except MultipleObjectsReturned:
        print(f"Найдено более одного ученика по имени {schoolkid_name}, "
              f"Укажите ФИО")
    except ObjectDoesNotExist:
        print(f"Ученик с именем {schoolkid_name} не найден")


def delete_chastisements(schoolkid_name):
    try:
        schoolkid_name = Schoolkid.objects.get(
            full_name__contains=schoolkid_name)
        chastisements = Chastisement.objects.filter(schoolkid=schoolkid_name)
        chastisements.delete()
    except MultipleObjectsReturned:
        print(f"Найдено более одного ученика по имени {schoolkid_name}, "
              f"Укажите ФИО")
    except ObjectDoesNotExist:
        print(f"Ученик с именем {schoolkid_name} не найден")


def create_commendation(schoolkid_name, subject_title):
    try:
        schoolkid = Schoolkid.objects.get(full_name__contains=schoolkid_name)
        subject = Lesson.objects.filter(subject__title=subject_title).first()
        if subject:
            lesson = Lesson.objects.filter(
                subject__title=subject_title,
                year_of_study=schoolkid.year_of_study,
                group_letter=schoolkid.group_letter)

            lesson_date = lesson.last().date
            teacher_name = lesson.first().teacher.full_name
            teacher = Teacher.objects.get(full_name=teacher_name)

            commendation = Commendation.objects.create(
                text=random.choice(COMMENDATION_TEXTS),
                created=lesson_date,
                schoolkid=schoolkid,
                subject=lesson.first().subject,
                teacher=teacher)

            return commendation
        else:
            print(f"Предмет с названием '{subject_title}' не найден")

    except MultipleObjectsReturned:
        print(f"Найдено более одного ученика по имени {schoolkid_name}, "
              f"Укажите ФИО")
    except ObjectDoesNotExist:
        print(f"Ученик с именем {schoolkid_name} не найден")
