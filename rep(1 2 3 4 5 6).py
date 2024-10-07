"""#задание 1
age = int(input("ваш возраст"))
if age < 18:
    print("вы несовершеннолетний")
elif 18< age <65:
    print("Вы трудоспособный человек")
elif 65 < age:
    print("вы пенсионер")
#задание 2
x = int(input("покупка"))
if x < 1000:
    print("нет скидки")
elif 1000 < x < 5000:
    print("скидка 5%")
elif 5000 < x:
    print("скидка 10%")
#задание 3
a = int(input())
b = int(input())
c = int(input())
if c == 1:
    print(a+b)
elif c == 2:
    print(a-b)
elif c == 3:
    print(a*b)
elif c == 4:
    print(a/b)
else:
    print("ошибка")
#задание 4
d = int(input())
if d % 10 == 2 or d % 10 == 6:
    print("TRUE")
else:
    print("FALSE")

#ЗАДАНИЕ 5
password = input()
f = input()
if password == password:
    print("доступ разрешен")
else:
    print("неверный пароль")"""
#задание 6
x = input("Введите координаты квадрата: ")
if x == "B1" or x == "B3" or x == "B7"  or x == "C1" or x == "C4" or x == "C5" or x == "C6" or x == "C8" or x == "C9":
    print("В данном квадрате обитает синий попугай")
elif x == "B2" or x == "B4" or x == "B6" or x == "B8" or x == "C2" or x == "C7" or x == "C10" or x == "C11":
    print ("В данном квадрате обитает зеленый попугай")
elif x == "B5" or x == "C3" or x == "C12":
    print("пустой, на нём никто не сидит")




