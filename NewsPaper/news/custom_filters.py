from django import template
from django.utils.safestring import mark_safe

register = template.Library()

# Список нецензурных слов (можно расширить)
BAD_WORDS = ['редиска', 'нехороший', 'плохой']

@register.filter(name='censor')
def censor(value):
    if not isinstance(value, str):
        raise ValueError("Фильтр 'censor' применяется только к строкам.")

    for word in BAD_WORDS:
        # Заменяем слово на звёздочки
        value = value.replace(word, word[0] + '*' * (len(word) - 1))
        value = value.replace(word.capitalize(), word[0].capitalize() + '*' * (len(word) - 1))

    return mark_safe(value)