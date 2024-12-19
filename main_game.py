import os
import sys
import threading
from guess_the_tune import GuessTheTuneGame


def start_game():
    print("\nДобавтье треки в папку '/sounds', после чего введите имена игроков через запятую!"
          "\n(корректный ввод должен содержать ровно три имени игрока)"
          "\n -> ", end='')
    players = input().strip().replace(" ", "").split(',')
    if len(players) != 3:
        print("Ошибка: должно быть ровно 3 игрока.")
        sys.exit(1)

    # Получаем все mp3 файлы из папки sounds
    sounds_folder = "sounds"
    tunes = []
    correct_answers = {}

    # Проверяем, существует ли папка sounds
    if not os.path.exists(sounds_folder):
        print(f"Папка '{sounds_folder}' не найдена.")
        sys.exit(1)

    # Получаем все mp3 файлы в папке sounds
    for filename in os.listdir(sounds_folder):
        if filename.endswith(".mp3"):
            tune = filename  # полное имя файла с расширением .mp3
            tunes.append(tune)
            correct_answers[tune] = filename[:-4]  # удаляем расширение .mp3 для правильного ответа

    if not tunes:
        print(f"В папке '{sounds_folder}' нет файлов MP3.")
        sys.exit(1)

    game = GuessTheTuneGame(players, tunes)
    game.correct_answers = correct_answers

    print("Добро пожаловать в игру 'Угадай мелодию'!")
    print("Для выхода введите команду 'exit'.")

    while True:
        try:
            tune = game.play_next_tune()
            correct_answer = game.correct_answers[tune]
            masked_answer = game.mask_correct_answer(correct_answer)

            current_player = players[(game.current_turn - 1) % len(players)]
            print(f"Сейчас играет: {masked_answer}. Игрок: {current_player}, ваш ответ?")

            # Запускаем мелодию в отдельном потоке
            music_thread = threading.Thread(target=game.play_tune, args=(tune,))
            music_thread.start()

            # Получаем ответ пользователя или команду 'exit'
            answer = input().strip()

            if answer.lower() == 'exit':
                print("Выход из игры...")
                game.stop_tune()  # Останавливаем музыку перед выходом
                music_thread.join()  # Ждем завершения потока
                break  # Прерываем игру

            game.stop_tune()  # Останавливаем воспроизведение после ввода ответа
            music_thread.join()  # Ждём завершения потока

            if game.submit_answer(current_player, answer):
                print("Правильно!")
            else:
                print("Неверно!")
        except Exception as e:
            print(str(e))
            break

    print("Игра окончена!")
    print("Результаты:")
    for player, score in game.scores.items():
        print(f"{player}: {score}")

    print(f"Победитель: {game.get_winner()}")


if __name__ == '__main__':
    start_game()
