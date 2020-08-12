"""
Вычисление времени прочтения статьи.

Среднестатистический человек читает 265 слов/мин.
Исключение для китайского, японского и корейского языков (500 символов/мин)
"""

from django import template
from django.utils.translation import gettext_lazy as _

import readtime

register = template.Library()

def read(text):
    ret = readtime.of_text(text).minutes
    last_dig = ret % 10
    if last_dig == 1:
        min = " минута"
    elif last_dig in [2, 3, 4]:
        min = " минуты"
    else: 
        min = " минут"
    return str(ret) + min

register.filter("readtime", read)
