import random
import math
random.seed(42) # Фиксируем seed, чтобы игра вела себя одинаково при каждом запуске

CRIMINAL = "ivanov"
TOTAL_CLUES = 4
MIN_CLUES_TO_WIN = 3
# Списки для хранения перечислений 
ROOMS = ["flat", "street", "cafe", "office", "police", "warehouse"]
SUSPECTS = ["petrov", "ivanov", "kuznetsova", "chernov"]
# Словари: ключ -> значение. 
# Заменяют длинные цепочки if/elif
# Описание каждой локации
DESCRIPTIONS = {
    "flat":      "Квартира Иванова. Скромно, но чисто, не вызывает подозрений.",
    "street":    "Улица возле ювелирного магазина. На мокром асфальте грязь.",
    "cafe":      "Кафе напротив. На столике у окна стоит стакан.",
    "office":    "Офис Чернова. Стол, компьютер, бумаги. Ничего необычного.",
    "police":    "Полицейский участок, в котором работает Кузнецова. На столе записка.",
    "warehouse": "Склад на окраине. Пахнет пылью и какой-то гнилью.",
}
# Какая улика лежит в локации (None = пусто)
CLUE_ITEMS = {
    "flat":      None,
    "street":    "грязные следы",
    "cafe":      "стакан с отпечатками губ",
    "office":    None,
    "police":    "записка",
    "warehouse": "перчатка",
}
# Варианты ответов подозреваемых (кортежи строк)
REPLIES = {
    "petrov":     ("У вас нет доказательств того, что это был я.", "Я был дома, спите спокойно."),
    "ivanov":     ("Я ничего не знаю. У вас нет ничего против меня.", "Вы тратите мое время."),
    "kuznetsova": ("Это была не я. Меня подставили.", "Я вообще не знаю этого человека."),
    "chernov":    ("Вы вышли не на того человека. Я не виновен.", "Мне нечего вам сказать."),
}
# Множества для проверки на уникальность 
visited = set()
taken = set()
# Текущее состояние игры 
place = ""
clues = []
# Добавляет улику в список и возвращает обновленный список.
def add_clue(clues, c):
    clues.append(c)
    return clues
# Добавляет подозреваемого в множество и возвращает его.
def add_suspect(suspects, s):
    suspects.add(s)
    return suspects
# Возвращает описание локации из словаря (или заглушку, если локации нет).
def describe(place):
    return DESCRIPTIONS.get(place, "Нет такой локации.")
# Проверяет, существует ли такая локация в списке ROOMS.
def is_valid_room(name):
    return name in ROOMS
# Возвращает название улики в локации или None, если улик нет.
def clue_in_room(place):
    return CLUE_ITEMS.get(place)
# Проверяет, хватает ли собранных улик для победы.
def has_enough_clues(clues, need=MIN_CLUES_TO_WIN):
    return len(clues) >= need
# ГЕНЕРАТОР СПИСКА (базовый): создает список подписей для каждого подозреваемого.
def suspect_labels(suspects):
    return [f"Подозреваемый: {s}" for s in suspects]
# ГЕНЕРАТОР СПИСКА (с условием): оставляет только улики длиннее 6 символов.
def long_clues(clues):
    return [c for c in clues if len(c) > 6]
# Генератор списка: возвращает локации, откуда еще не забрали улики.
def rooms_without_clues(visited, taken):
    return [r for r in ROOMS if r not in taken]

def show_help(): # Функция для вызова сводки по командам
    print("Доступные команды: ")
    print("help -          открывает список команд.")
    print("look -          осмотреть локацию.")
    print("go -            пойти на локацию.")
    print("take -          подобрать улику.")
    print("talk            <name> - поговорить с подозреваемым (например, talk ivanov).")
    print("accuse <name> - обвинить подозреваемого (например, accuse ivanov).")
    print("exit -          завершить игру.")

def exit_game(): # Функция для выхода из игры
    print("До встречи, следователь!")

def go_to(current_place): # Функция для перехода на локацию
    # Спрашивает у игрока новую локацию и проверяет её на существование.
    print(f"Доступные локации: {', '.join(ROOMS)}.")  
    new_place = input("Вы хотите пойти на локацию: ").strip().lower()
    if is_valid_room(new_place):
        print(f"Вы перешли на локацию: {new_place}")
        return new_place
    else:
        print(f"Такой локации нет.")
        return current_place 

def look_around(place, visited, clues): # Функция для осмотра локации
    # Осматривает локацию, находит улику и добавляет её в список.
    # 1. Если игрок ещё никуда не пошёл
    if place == "":
        print("Вы пока нигде. Используйте 'go', чтобы перейти на локацию.")
        return clues, visited
    # Если уже осматривали
    if place in visited:
        print("Здесь вы уже всё осмотрели.")
        return clues, visited # если место уже осмотрено, возвращаемся к тому, что было, без изменений
    # Отмечаем, что осмотрели (добавляем в МНОЖЕСТВО)
    visited.add(place)
    # Печатаем описание
    print(f"Вы осматриваете локацию: {place}")
    print(describe(place))
    # Проверяем улику
    clue = clue_in_room(place)
    if clue is not None:
        print(f"Вы нашли {clue}.")
        if place == "street":
            clues.append(clue) # На улице улика берется сразу, в других местах — через take
            print(f"Вы забрали улику. Собрано улик {len(clues)}.")
        else:
            print("Используйте команду take, чтобы забрать.")
    else:
        print("Здесь больше нечего брать.")
    return clues, visited

def take_clue(place, clues, visited, taken):
    if place == "":
        print("Вы пока нигде. Используйте 'go', чтобы перейти на локацию.")
        return clues, visited, taken
    # Забирает улику из локации, если она была осмотрена.
    # Проверки: есть ли локация, осмотрена ли она, не забрали ли уже
    if place not in visited:
        print("Вы ещё не осматривали эту локацию.")
        return clues, visited, taken

    if place in taken:
        print("Вы уже забрали отсюда улику.")
        return clues, visited, taken

    clue = clue_in_room(place)
    if clue is not None:
        # Если все хорошо, добавляем в список и отмечаем в множестве
        clues.append(clue)
        taken.add(place)
        print(f"Вы подобрали улику: {clue}! Собрано улик: {len(clues)}")
        
        if len(clues) >= MIN_CLUES_TO_WIN:
            print(">>> У вас достаточное количество улик. Вы можете обвинить кого-то сейчас или осмотреть оставшиеся локации. Используйте команду accuse <name>.")
            print(">>> Вы можете поговорить с подозреваемыми. Используйте команду talk <name>.")
            
        if len(clues) == TOTAL_CLUES:
            print(">>> Вы осмотрели все доступные локации и собрали все улики!")
    else:
        print("Здесь нет улик, которые можно было бы взять.")
        
    return clues, visited, taken

def talk_to(suspect_name, clues):
    # Выводит реплику подозреваемого. Иванов сознается при наличии всех улик.
    # Проверяем, есть ли такой подозреваемый в нашем списке SUSPECTS
    if suspect_name not in SUSPECTS:
        print("Нет такого подозреваемого.")
        return
    # Особая логика для Иванова, если собраны все улики
    if suspect_name == "ivanov" and len(clues) == TOTAL_CLUES:
        print("Иванов: Ладно, признаюсь, это был я.")
        print(">>> Теперь у вас есть все, чтобы обвинить Иванова. Используйте 'accuse ivanov' <<<")
        return
    # Получаем кортеж с репликами из словаря (или пустой кортеж, если вдруг имени нет)
    replies = REPLIES.get(suspect_name, ("...",))
    # random.choice выбирает случайную фразу из кортежа
    print(f"{suspect_name.capitalize()}: {random.choice(replies)}")

def accuse(accused_name, criminal_name, clues, total_clues=4): # Функция для обвинения подозреваемого
    # Обвиняет подозреваемого. Возвращает True, если игра окончена, иначе False.
    # Считаем нужное количество улик (75% от общего числа)
    needed_clues = math.ceil(total_clues * 0.75)
    # Проверки...
    if accused_name not in SUSPECTS:
        print("Нет такого подозреваемого.")
        return False
    if accused_name != criminal_name:
        print(f"Вы обвинили {accused_name}, но это не он. Вы проиграли.")
        return True  # Возвращаем True, потому что игра окончена (проигрыш)
    # Если имя совпало, проверяем улики. 
    if len(clues) >= needed_clues:
        print(f"Вы обвинили {accused_name}. Вы собрали достаточно улик ({len(clues)}). Вы победили!")
        return True
    else:
        print(f"Вы обвинили {accused_name}. Это был правильный выбор, но улик ({len(clues)}) было меньше, чем нужно ({needed_clues}). Судья отпустил преступника. Вы проиграли.")
        return True  # Игра окончена (победа или поражение из-за нехватки улик)