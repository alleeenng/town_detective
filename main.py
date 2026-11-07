import game_data as gd
# Цикл для всей игры
def main():
    player = input("Ваше имя:")
    print(f"Добро пожаловать, {player}! Ваша цель: собрать {gd.MIN_CLUES_TO_WIN} улики и обвинить преступника.")
    print("Ночью произошло ограбление в ювелирном магазине.")
    print("Подозреваемые: Петров(petrov), Иванов(ivanov), Кузнецова(kuznetsova), Чернов(chernov).")
    print("Чтобы обвинить преступника, используйте команду accuse <name>.")
    print("Всего можно собрать 4 улики. Удачи, детектив!")
        
    print(f"Собрано улик: {gd.clues}")
    print(f"Вы не находитесь ни на какой локации {gd.place}")
    print("Чтобы открыть список команд, введите 'help'")
    
    while True:
        command = input("> ").strip().lower()

        # Справка по командам
        if command == "help":
            gd.show_help()

            # Выход из игры
        elif command == "exit":
            gd.exit_game()
            break

        # Перемещение между локациями
        elif command == "go":
            gd.place = gd.go_to(gd.place)

        # Осмотр текущей локации
        elif command == "look":
            gd.clues, gd.visited = gd.look_around(gd.place, gd.visited, gd.clues)

            # Подбор улики на текущей локации
        elif command == "take":
            gd.clues, gd.visited, gd.taken = gd.take_clue(gd.place, gd.clues, gd.visited, gd.taken)

            # Разговор с подозреваемыми
        elif command.startswith("talk "):
                # Отрезаем слово "talk " и берем имя
            gd.suspect = command[5:].strip()    
            # Вызываем функцию talk_to и передаем туда имя и улики
            gd.talk_to(gd.suspect, gd.clues)
            
            # Обвинение подозреваемого
        elif command.startswith("accuse "):
                # Отрезаем слово "accuse " (7 символов) и берем имя
            gd.suspect = command[7:].strip()
                    
                # Вызываем функцию и ловим результат (True = игра окончена)
            is_game_over = gd.accuse(gd.suspect, gd.CRIMINAL, gd.clues, gd.total_clues)
                    
            if is_game_over:
                    break  # Выходим из цикла, игра завершена

            else: 
                print("Неизвестная команда. Введите 'help'.")

# Точка входа
if __name__ == "__main__":
    main()