import random
import string
from faker import Faker
faker = Faker()

class DataGenerator:
    @staticmethod
    def generate_random_email():
        random_string = ''.join(random.choices(string.ascii_lowercase + string.digits, k=7))
        return f'kekk{random_string}@gmail.com'

    @staticmethod
    def generate_random_name():
        return f'{faker.first_name()} {faker.last_name()}'


    @staticmethod
    def generate_random_password():
        """
        Генерация пароля, соответствующего требованиям:
        - Минимум 1 буква.
        - Минимум 1 цифра.
        - Допустимые символы.
        - Длина от 8 до 20 символов.
        """
        letters = random.choices(string.ascii_lowercase, k=1)
        upper = random.choices(string.ascii_uppercase, k=1)
        digits = random.choices(string.digits, k=4)
        special_chars = "?@#$%^&*|:"
        all_chars = string.ascii_letters + string.digits + special_chars
        count_number = random.randint(2, 14)
        remaining_chars = random.choices(all_chars, k=count_number)
        password = letters + upper + digits + remaining_chars
        random.shuffle(password)
        return ''.join(password)
