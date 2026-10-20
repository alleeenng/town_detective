player = input("Ваше имя:")
print(f"Добро пожаловать, {player}! Ваша цель: собрать минимум три улики и обвинить преступника.")
print("Ночью произошло ограбление в ювелирном магазине.")
print("Подозреваемые: Петров(petrov), Иванов(ivanov), Кузнецова(kuznetsova), Чернов(chernov).")
print("Чтобы обвинить преступника, используйте команду accuse <name>.")
print("Всего можно собрать 4 улики. Удачи, детектив!")

place = "street"
clues = 0
visited = []
taken = []
criminal = "ivanov"
total_clues = 4

print(f"Собрано улик: {clues}")
print("Чтобы открыть список команд, введите 'help'")
print(f"Вы находитесь на локациии: {place}")

while True:
    command = input("> ")

    if command == "help":
        print("Доступные команды: help, look, go, talk <name>, exit")
        print("help - открывает список команд.")
        print("look - осмотреть локацию.")
        print("go - пойти на локацию.")
        print("talk - поговорить с подозреваемым.")
        print("С помощью команды exit вы можете завершить игру.")
        
    if command == "exit":
        print("До встречи, следователь!")
        break

    if command == "go":
               print("Доступные локации: flat, street, cafe, office, police, warehouse.")  
               place = input('Вы хотите пойти на локацию:')

    if command == "look":

        if place == "flat":
            print("Вы осмотрели квартиру Иванова и, к сожалению, ничего не нашли.")
            if place not in visited and place not in taken:
                visited.append(place)
            else:
                print("Здесь вы уже все осмотрели.")
    

        elif place == "street":
            print("Вы осмотрели улицу и нашли грязные следы от чьей-то обуви.")
            if place not in visited and place not in taken:
                clues += 1
                visited.append(place)
                print(f"Собрано улик: {clues}")
            else:
                 print("Здесь вы уже все осмотрели.")

        elif place == "cafe":
            print("Вы зашли в кафе Петрова, осмотрели его и нашли стакан с отпечатками губной помады. Используйте команду take, чтобы забрать его.")

            if "cafe" not in visited and place not in taken:
                visited.append(place)
            else:
                print("Здесь вы уже все осмотрели.")

        elif place == "office":
            print("Вы осмотрели офис, в котором работает Чернов, и, к сожалению, ничего не нашли.")
            if place not in visited not in taken:
                visited.append(place)
            else:
                print("Здесь вы уже все осмотрели.")

        elif place == "warehouse":
            print("Вы осмотрели склад и нашли перчатку с инициалами 'И**'. Используйте take, чтобы поднять.")
            if place not in visited and place not in taken:
                visited.append(place)
            else:
                print("Здесь вы уже все осмотрели.")

        elif place == "police":
            print("В полицейском участке на столе Кузнецовой вы записку, на которой были пыльные отпечатки пальцев. Используйте take, чтобы взять записку.")
            if place not in visited and place not in taken:
                visited.append(place)
            else:
                print("Здесь вы уже все осмотрели.")

    elif command == "take":
        if place in visited and place not in taken:
            clues += 1
            print(f"Вы подобрали улику! Собрано улик: {clues}")
            visited.remove(place)
            taken.append(place)

            if clues >= 3:
                print(">>> У вас достаточное количество улик. Вы можете обвинить кого-то сейчас или осмотреть оставшиеся локации. Используйте команду accuse <name>.")

            if clues == total_clues:
                print(">>> Вы осмотрели все доступные локации и собрали все улики!")
                print(">>> Вы можете поговорить с подозреваемыми. Используйте команду talk <name>.")
            
        else:
            print("Здесь больше нечего брать.")

    elif command == "talk ivanov":

        if clues == total_clues:
            print("Иванов: Ладно, признаюсь, это был я.")
            print(">>> Теперь у вас есть все, чтобы обвинить Иванова. Используйте 'accuse ivanov' <<<")
        else:
            print("Иванов: Я ничего не знаю. У вас нет ничего против меня.")

    elif command == "talk petrov":
        print("Петров: У вас нет доказательств того, что это был я.")

    elif command == "talk kuznetsova":
        print("Кузнецова: Это была не я. Меня подставили!")

    elif command == "talk chernov":
        print("Чернов: Вы вышли не на того человека. Я не виновен.")

    if command == "accuse petrov":
        print("Вы обвинили не того человека и проиграли.")
        break

    elif command == "accuse ivanov" and clues >= 3:
        print("Вы собрали нужное количество улик и обвинили преступника. Вы победили!")
        break

    elif command == "accuse ivanov" and clues < 3:
        print("Вы обвинили правильного человека, но не собрали нужное количество улик, и судья отпустил преступника. Вы проиграли.")
        break

    elif command == "accuse kuznetsova":
        print("Вы обвинили не того человека и проиграли.")
        break

    elif command == "accuse chernov":
        print("Вы обвинили не того человека и проиграли.")
        break