import random


def generate_verification_code():
    """
    Генерация кода авторизации
    """
    return ''.join([random.choice(list('1234567890')) for x in range(4)])


def send_verification_code(verification_code, **kwargs):
    """
        Метод для отправки кода авторизации на указанный пользователем номер телефона
    """

    print(f'Код авторизации: {verification_code}')