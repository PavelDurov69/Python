#задание1
def alpha(inp: str):
    inp = list(inp)
    abc = list("абвгдеёжзийклмнопрстуфхцчшщъыьэюя")
    out = []
    for i in inp:
        if i in abc:
            out.append(i)
            abc.remove(i)
    out += abc
    return out


print(alpha("пайтон"))

#задание2
def calendar(name: str, year: int, days: int):
    print(f"Календарь: {name} {year}")
    for i in range(days):
        if (i + 1) % 7 == 0:
            print(i + 1, end="\n")
        else:
            print(i + 1, end=" ")


calendar("Чехословакия", 2045, 23)

#задание3
def bin_sys(a: int, b: int):
    n = b - a + 1
    sumout = 0
    for i in range(n):
        out = bin(i + a)
        sumout += i + a
        out = out[2::]
        print(out)
    sumout = bin(sumout)[2::]
    print(f"Сумма: {sumout}")


bin_sys(3, 6)

#задание4
def star(lst: list, row: int, elem: int):
    lst[row][elem] = " * "
    print(lst[0])
    print(lst[1])
    print(lst[2])


field = [["[ ]", "[ ]", "[ ]"],
         ["[ ]", "[ ]", "[ ]"],
         ["[ ]", "[ ]", "[ ]"]]
star(field, 2, 1)

#задание5
def numbers(n: int, i=1):
    print(f"[{n}] [{n + 1 * i}]\n[{n + 2 * i}] [{n + 3 * i}]")


numbers(1, 2)

#задание6
def exam(string: str, letter: str) -> int:
    n = 0
    for i in string:
        if i.capitalize() == letter.capitalize():
            n += 1
    return n


print(exam("My name is Sara.", "s"))

