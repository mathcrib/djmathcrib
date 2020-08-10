"""
Вычисление времени прочтения статьи.

Среднестатистический человек читает 265 слов/мин.
Исключение для китайского, японского и корейского языков (500 символов/мин)
"""

import readtime
from django import template
from django.utils.translation import gettext_lazy as _

register = template.Library()

def read(text):
    return readtime.of_text(text).minutes

register.filter("readtime", read)
