#задание1
x = lambda a, b: a * b
print(x(2, 3))

#задание2
n = int(input("Введите количество чисел: "))
list1 = []
for i in range(n):
    list1.append(int(input(f"Введите число {i + 1}: ")))
list1 = list(filter(lambda a: (a % 3 == 0), list1))
print(list1)
