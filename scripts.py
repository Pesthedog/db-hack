from datacenter.models import Chastisement, Commendation, Schoolkid, Lesson, Mark
import random
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned


def fix_marks(schoolkid):
    bad_marks = Mark.objects.filter(schoolkid=schoolkid, points__lt=4)
    for mark in bad_marks:
        mark.points = 5
        mark.save()


def remove_chastisements(schoolkid):
    chastisements = Chastisement.objects.filter(schoolkid=schoolkid)
    for chastisement in chastisements:
        chastisement.delete()


def create_commendation(kid_name, subject):
    try:
        schoolkid = Schoolkid.objects.get(full_name=kid_name)
    except MultipleObjectsReturned:
        return "Найдено несколько учеников. Введите фио ученика."
    except ObjectDoesNotExist:
        return "Ученик с таким именем не найден."

    lesson = Lesson.objects.filter(year_of_study=schoolkid.year_of_study, group_letter=schoolkid.group_letter,
                                   subject__title=subject).order_by('-date').first()

    commendation_text_list = ["Молодец!", "Отлично!", "Хорошо!",
                              "Ты меня очень обрадовал!", "Лучше чем я ожидал!", "Ты сегодня прыгнул выше головы!",
                              "Так держать!", "Превосходно!"]

    Commendation.objects.create(text=random.choice(commendation_text_list), created=lesson.date, schoolkid=schoolkid,
                                subject=lesson.subject, teacher=lesson.teacher)
