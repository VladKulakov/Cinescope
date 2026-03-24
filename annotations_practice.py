from typing import List, Union, Optional



#
# def multiply(a: int, b: int) -> int :
#     return a * b
#
# print(multiply(5,2))
#
# def sum_numbers(numbers: List[int]) -> int:
#     return sum(numbers)
#
#
# print(sum_numbers([1, "dfs", 10]))

# def find_user(user_id: int) -> Optional[str]:
#     if user_id == 1:
#         return "Пользователь найден"
#     return None
#
#
# print(find_user(1))
#
# def process_input(value:Union[str, int]) -> str:
#     return f"Ты передал: {value}"
#
#
# print(process_input(2345234.2342))

# class User:
#     def __init__(self, name: str, age: int):
#         self.name = name
#         self.age = age
#
#     def greet(self) -> str:
#         return f"Привет, меня зовут {self.name}!"
#
# neee = User("Артем", 25).greet()
# print(neee)


# from typing import List
#
# def get_even_numbers(numbers: List[int]) -> List[int]:
#     return [num for num in numbers if num % 2 == 0]
#
# wrong_numbers = [1, "two", 3, "four", 5, "six", 7, "eight", 9, "ten"]
# try:
#     even_numbers = get_even_numbers(wrong_numbers)
#     print(f"Четные числа: {even_numbers}")
# except TypeError as e:
#     print(f"Ошибка: {e}")
