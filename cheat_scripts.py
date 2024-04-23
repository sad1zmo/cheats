from datacenter.models import Schoolkid
from datacenter.models import Mark
from datacenter.models import Chastisement
from datacenter.models import Lesson
from datacenter.models import Commendation
from datacenter.models import Teacher
import random
from django.core.exceptions import MultipleObjectsReturned, ObjectDoesNotExist


def fix_marks(schoolkid_name):
    schoolkid_name = Schoolkid.objects.get(full_name__contains=schoolkid_name)
    bad_marks = Mark.objects.filter(schoolkid=schoolkid_name, points__lt=4)

    for bad_mark in bad_marks:
        bad_mark.points = 5
        bad_mark.save()


def delete_chastisements(schoolkid_name):
    schoolkid_name = Schoolkid.objects.get(full_name__contains=schoolkid_name)
    chastisements = Chastisement.objects.filter(schoolkid=schoolkid_name)
    chastisements.delete()


def create_commendation(schoolkid_name, subject_title):
    try:
        schoolkid = Schoolkid.objects.get(full_name__contains=schoolkid_name)
        subject = Lesson.objects.filter(subject__title=subject_title).first()
        if subject:
            math_lessons_6a = Lesson.objects.filter(
                subject__title=subject_title,
                year_of_study=6,
                group_letter='А')
            teacher_name = math_lessons_6a.first().teacher.full_name
            teacher = Teacher.objects.get(full_name=teacher_name)

            lesson_date = Lesson.objects.filter(
                teacher__full_name__contains=teacher_name,
                subject__title=subject_title,
                year_of_study=6,
                group_letter='А').last().date

            commendation_text = ['Молодец!', 'Отлично!', 'Хорошо!',
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

            commendation = Commendation.objects.create(
                text=random.choice(commendation_text),
                created=lesson_date,
                schoolkid=schoolkid,
                subject=math_lessons_6a.first().subject,
                teacher=teacher)

            return commendation
        else:
            print(f"Предмет с названием '{subject_title}' не найден")

    except MultipleObjectsReturned:
        print(f"Найдено более одного ученика по имени {schoolkid_name}, "
              f"Укажите ФИО")
    except ObjectDoesNotExist:
        print(f"Ученик с именем {schoolkid_name} не найден")
