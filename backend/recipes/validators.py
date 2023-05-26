from django.core.validators import RegexValidator


class WordNameValidator(RegexValidator):
    regex = r'^[а-яА-ЯёЁa-zA-Z0-9 -]+$'
    message = (
        'Имя должно включать только буквы, '
        'цифры, пробел и дефис.'
    )


class ColorValidator(RegexValidator):
    regex = '^#([A-Fa-f0-9]{3,6})$'
    message = 'Введенное значение не является HEX-кодом!'
