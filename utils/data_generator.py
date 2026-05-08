import datetime
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
    def generate_user_data() -> dict:
        """Генерирует данные для тестового пользователя"""
        from uuid import uuid4

        return {
            'id': f'{uuid4()}',  # генерируем UUID как строку
            'email': DataGenerator.generate_random_email(),
            'full_name': DataGenerator.generate_random_name(),
            'password': DataGenerator.generate_random_password(),
            'created_at': datetime.datetime.now(),
            'updated_at': datetime.datetime.now(),
            'verified': False,
            'banned': False,
            'roles': '[USER]'
        }

    @staticmethod
    def generate_movies_data() -> dict:
        """Генерирует данные для тестового пользователя"""

        return {
            'id': random.randint(10000, 999999),# генерируем UUID как строку
            "name": "ab" + faker.unique.word().capitalize(),
            "price": faker.random_int(100, 1000),
            "description": faker.paragraph(1),
            "image_url": faker.image_url(),
            "location": faker.random_element(elements=["MSK", "SPB"]),
            "published": True,
            "rating": round(random.uniform(0, 5), 1),
            "genre_id": 6,
            "created_at": datetime.datetime.now()
        }

    @staticmethod
    def generate_random_int(number: int) -> int:
        return random.randint(1, number)

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

    @staticmethod
    def generate_movies():
        return {
            "name": faker.unique.word().capitalize(),
            "imageUrl": faker.image_url(),
            "price": faker.random_int(100, 1000),
            "description": faker.paragraph(1),
            "location": faker.random_element(elements=["MSK", "SPB"]),
            "published": True,
            "genreId": faker.random_int(1, 10)
        }
    @staticmethod
    def price_range():
        """Фикстура с рандомным диапазоном цен, где min_price < max_price."""
        min_price = random.randint(1, 500)
        max_price = random.randint(min_price + 1, min_price + 500)
        return {
            "min_price": min_price,
            "max_price": max_price
        }

    @staticmethod
    def gen_locations():
        location = random.choice(["MSK", "SPB"])
        return {"locations": location}

    @staticmethod
    def pagesize():
        number = random.randint(1, 20)
        return {"pageSize": number}

    @staticmethod
    def generate_random_genreld():
        number = random.randint(1,3)
        return {"genreld": number}

    @staticmethod
    def negative_pagesize():
        number = random.randint(30, 40)
        return {"pageSize": number}

    @staticmethod
    def invalid_price_range():
        min_price = random.randint(1, 500)
        max_price = random.randint(min_price + 1, min_price + 500)
        return {"minPrice": max_price, "maxPrice": min_price}

    @staticmethod
    def negative_locations():
        return {"locations": "USA"}