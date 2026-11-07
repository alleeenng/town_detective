CRIMINAL = "ivanov"
TOTAL_CLUES = 4
MIN_CLUES_TO_WIN = 3
visited = ""
taken = ""
total_clues = TOTAL_CLUES
place = ""
clues = 0
import random
import math

random.seed(42) # Фиксируем seed, чтобы игра вела себя одинаково при каждом запуске
def show_help(): # Функция для вызова сводки по командам
    print("Доступные команды: help, look, go, talk <name>, exit")
    print("help - открывает список команд.")
    print("look - осмотреть локацию.")
    print("go - пойти на локацию.")
    print("talk - поговорить с подозреваемым.")
    print("С помощью команды exit вы можете завершить игру.")

def exit_game(): # Функция для выхода из игры
    print("До встречи, следователь!")

def go_to(current_place): # Функция для перехода на локацию
    print("Доступные локации: flat, street, cafe, office, police, warehouse.")  
    new_place = input("Вы хотите пойти на локацию: ").strip().lower()
    if (new_place == "flat" or new_place == "street" or new_place == "cafe" or 
        new_place == "office" or new_place == "police" or new_place == "warehouse"):
        print(f"Вы перешли на локацию: {new_place}")
        return new_place
    else:
        print(f"Такой локации нет.")
        return current_place 

def look_around(place, visited, clues): # Функция для осмотра локации
    print(f"Вы осматриваете локацию: {place}")

    if place in visited:
        print("Здесь вы уже всё осмотрели.")
        return clues, visited # если место уже осмотрено, возвращаемся к тому, что было, без изменений
    visited = visited + place + " "

    if place == "street":
        print("Вы осмотрели улицу и нашли грязные следы от чьей-то обуви.")
        clues += 1  # На улице улика дается сразу
        print(f"Собрано улик: {clues}")
        
    elif place == "flat":
        print("Вы осмотрели квартиру Иванова и ничего не нашли.")
        
    elif place == "cafe":
        print("Вы нашли стакан с отпечатками. Используйте команду take, чтобы забрать его.")
        
    elif place == "office":
        print("Вы осмотрели офис Чернова и ничего не нашли.")
        
    elif place == "warehouse":
        print("Вы нашли перчатку. Используйте take, чтобы поднять.")
        
    elif place == "police":
        print("Вы нашли записку. Используйте take, чтобы взять.")

    return clues, visited

def take_clue(place, clues, visited, taken): # Функция для подбора улики
    if place in visited and place not in taken:
        clues += 1
        print(f"Вы подобрали улику! Собрано улик: {clues}")

        visited = visited.replace(place + " ", "")

        taken = taken + place + " "
# улика забрана — убираем из "осмотренных"
# помечаем локацию как обысканную

# Подсказка, когда улик достаточно для обвинения
        if clues >= 3:
            print(">>> У вас достаточное количество улик. Вы можете обвинить кого-то сейчас или осмотреть оставшиеся локации. Используйте команду accuse <name>.")
            print(">>> Вы можете поговорить с подозреваемыми. Используйте команду talk <name>.")
# Подсказка, когда собраны все улики
        if clues == 4:
            print(">>> Вы осмотрели все доступные локации и собрали все улики!")            
        else:
            print("Здесь больше нечего брать.")

    return clues, visited, taken

def talk_to(suspect_name, clues, total_clues=4): # Функция для разговора с подозреваемыми
    if(suspect_name != "petrov" and suspect_name != "ivanov" and 
       suspect_name != "kuznetsova" and suspect_name != "chernov"):
        print("Нет такого подозреваемого.")
        return
    
    if suspect_name == "ivanov" and clues == total_clues:
        print("Иванов: Ладно, признаюсь, это был я.")
        print(">>> Теперь у вас есть все, чтобы обвинить Иванова. Используйте 'accuse ivanov' <<<")
        return

    if suspect_name == "petrov":
        replies = ("У вас нет доказательств того, что это был я.", "Я был дома, спите спокойно.")
    elif suspect_name == "kuznetsova":
        replies = ("Это была не я. Меня подставили!", "Я вообще не знаю этого человека.")
    elif suspect_name == "chernov":
        replies = ("Вы вышли не на того человека. Я не виновен.", "Мне нечего вам сказать.")
    else: # Для Иванова, если улик мало
        replies = ("Я ничего не знаю. У вас нет ничего против меня.", "Вы тратите мое время.")

    # Выбираем случайную фразу из кортежа и печатаем
    print(f"{suspect_name.capitalize()}: {random.choice(replies)}")

def accuse(accused_name, criminal_name, clues, total_clues): # Функция для обвинения подозреваемого
    # Если игрок обвинил не того, кого нужно
    needed_clues = math.ceil(total_clues * 0.75)
    if accused_name != criminal_name:
        print(f"Вы обвинили {accused_name}, но это не он. Вы проиграли.")
        return True  # Возвращаем True, потому что игра окончена (проигрыш)
        
    # Если имя совпало, проверяем улики
    if clues >= needed_clues:
        print(f"Вы обвинили {accused_name}. Вы собрали достаточно улик ({clues}). Вы победили!")
        return True
    else:
        print(f"Вы обвинили {accused_name}. Это был правильный выбор, но улик ({clues}) было меньше, чем нужно ({needed_clues}). Судья отпустил преступника. Вы проиграли.")
        return True  # Игра окончена (победа или поражение из-за нехватки улик)