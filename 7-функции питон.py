#задание 1
def create_car(name: str, color: str, speed: int) -> str:
    return f"Марка: {name} Цвет: {color} Максимальная скорость: {speed}"


car1 = create_car("Лада", "Серый", 120)
car2 = create_car("Тойота", "Красный", 300)

print(car1)
print(car2)

#задание2
def switch_check(switch: bool):
    if switch == True:
        print("True работает")
    elif switch == False:
        print("False не работает")
    else:
        print(f"{switch} сломан.")


switch_1 = True
switch_2 = False
switch_3 = None

switch_check(switch_1)
switch_check(switch_2)
switch_check(switch_3)

#задание3
def triangle(a: float, b: float, c: float):
    if a + b > c and b + c > a and c + a > b:
        p = a + b + c
        s = p / 2
        area = (s * (s - a) * (s - b) * (s - c)) ** 0.5
        area = round(area, 2)
        if a == b == c:
            print(f"----------------------------------------\n"
                  f"Длина сторон треугольника:  {a}, {b}, {c}\n"
                  f"----------------------------------------\n"
                  f"Информация:\n"
                  f"Равносторонний треугольник\n"
                  f"Периметр: {p}\n"
                  f"Площадь: {area}\n"
                  f"----------------------------------------")
        elif a == b or b == c or c == a:
            print(f"----------------------------------------\n"
                  f"Длина сторон треугольника:  {a}, {b}, {c}\n"
                  f"----------------------------------------\n"
                  f"Информация:\n"
                  f"Равнобедренный треугольник\n"
                  f"Периметр: {p}\n"
                  f"Площадь: {area}\n"
                  f"----------------------------------------")
        else:
            print(f"----------------------------------------\n"
                  f"Длина сторон треугольника:  {a}, {b}, {c}\n"
                  f"----------------------------------------\n"
                  f"Информация:\n"
                  f"Разносторонний треугольник\n"
                  f"Периметр: {p}\n"
                  f"Площадь: {area}\n"
                  f"----------------------------------------")
    else:
        print("Некорректные стороны. Невозможно построить треугольник.")


triangle(15, 15, 15)  # 97.42785792574935
triangle(15, 20, 15)  # 111.80339887498948
triangle(15, 20, 25)  # 150.0
triangle(1, 2, 3)

#задание4
def number_change(input_number: int, output_number: int):
    i = 0
    if input_number > output_number:
        while input_number > output_number:
            input_number -= 1
            i += 1
    elif input_number < output_number:
        while input_number < output_number:
            input_number += 1
            i += 1
    else:
        i = 0
    return i, input_number, output_number


print(number_change(12, 4))
print(number_change(4, 12))
print(number_change(12, 12))

#задание5
player = 0


def info_player():
    print(f"Игрок пробежал {player} км.")


def run_player(km):
    global player
    player += km / 2


info_player()
run_player(30)
run_player(12.5)
info_player()

#задание6
def prime_check(x: int) -> bool:
    """
    Проводит тест простоты числа перебором.

    Параметры:
    x (int) - целое число

    Возвращает:
    True - если число простое
    False - если число не простое (включая отрицательные числа и нуль)

    Пример:
    >> prime_check(13)
    True
    >> prime_check(-1)
    False
    """
    if x < 2:  # Обработка исключений цикла
        return False

    i = 2
    while i < x:  # Тест простоты числа перебором
        if x % i != 0:
            i += 1
        else:
            return False
    else:
        return True


print(prime_check.__doc__)
print(prime_check(13))
print(prime_check(-1))
print(prime_check(103))
print(prime_check(2048))
