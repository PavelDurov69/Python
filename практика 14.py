#задание1
while True:
    x = input("Введите число: ")
    try:
        x = int(x)
    except ValueError:
        print(f"{x} - не число. Повторите ввод.")
    else:
        break
for i in range(x + 1):
    print(i, end=" ")

#задание2
list1 = [4, 43.5, 1.5, 31, 588, 320.1, 192.16]
for i, e in enumerate(list1):
    try:
        print(f"{e} / {i} = {e / i}")
    except ZeroDivisionError:
        print(f"Деление на ноль! Элемент: {e}")

  #задание3
  list1 = []
while len(list1) < 5:
    try:
        list1.append(int(input("Введите число: ")))
    except ValueError:
        print("Не число")
        continue
print(f"Числа в списке: {list1}")
