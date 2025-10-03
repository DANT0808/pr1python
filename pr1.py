print("Калькулятор")


try:
    a = int(input("Введите первое число: "))
    b = int(input("Введите второе число: "))
except ValueError:
    print("Ошибка: нужно вводить именно числа!")
    exit()

print("\nВыберите операцию:")


print("\nАрифметические операторы:")
print("1. +  (сложение)")
print("2. -  (вычитание)")
print("3. *  (умножение)")
print("4. /  (деление)")
print("5. // (целочисленное деление)")
print("6. %  (остаток от деления)")
print("7. ** (возведение в степень)")


print("\nОператоры сравнения:")
print("8. == (равно)")
print("9. != (не равно)")
print("10. > (больше)")
print("11. < (меньше)")
print("12. >= (больше или равно)")
print("13. <= (меньше или равно)")


print("\nЛогические операторы:")
print("14. and (логическое И)")
print("15. or  (логическое ИЛИ)")
print("16. not (логическое НЕ, применяется к первому числу)")


print("\nПобитовые операторы:")
print("17. &  (побитовое И)")
print("18. |  (побитовое ИЛИ)")
print("19. ^  (побитовое XOR)")
print("20. ~  (побитовое НЕ, применяется к первому числу)")
print("21. << (сдвиг влево)")
print("22. >> (сдвиг вправо)")


print("\nОператоры принадлежности:")
print("23. in     (цифра a содержится в числе b)")
print("24. not in (цифра a не содержится в числе b)")

print("\nОператоры тождественности:")
print("25. is     (тождественно)")
print("26. is not (не тождественно)")

choice = input("\nВведите номер операции: ")


if choice == "1":
    print("Результат:", a + b)
elif choice == "2":
    print("Результат:", a - b)
elif choice == "3":
    print("Результат:", a * b)
elif choice == "4":
    if b == 0:
        print("Ошибка: на ноль делить нельзя!")
    else:
        print("Результат:", a / b)
elif choice == "5":
    if b == 0:
        print("Ошибка: на ноль делить нельзя!")
    else:
        print("Результат:", a // b)
elif choice == "6":
    if b == 0:
        print("Ошибка: на ноль делить нельзя!")
    else:
        print("Результат:", a % b)
elif choice == "7":
    print("Результат:", a ** b)


elif choice == "8":
    print("Результат:", a == b)
elif choice == "9":
    print("Результат:", a != b)
elif choice == "10":
    print("Результат:", a > b)
elif choice == "11":
    print("Результат:", a < b)
elif choice == "12":
    print("Результат:", a >= b)
elif choice == "13":
    print("Результат:", a <= b)

elif choice == "14":
    print("Результат:", bool(a) and bool(b))
elif choice == "15":
    print("Результат:", bool(a) or bool(b))
elif choice == "16":
    print("Результат:", not bool(a))


elif choice == "17":
    print("Результат:", a & b)
elif choice == "18":
    print("Результат:", a | b)
elif choice == "19":
    print("Результат:", a ^ b)
elif choice == "20":
    print("Результат:", ~a)
elif choice == "21":
    print("Результат:", a << b)
elif choice == "22":
    print("Результат:", a >> b)


elif choice == "23":
    print("Результат:", str(a) in str(b))
elif choice == "24":
    print("Результат:", str(a) not in str(b))


elif choice == "25":
    print("Результат:", a is b)
elif choice == "26":
    print("Результат:", a is not b)

else:
    print("Ошибка: неверный пункт меню!")
