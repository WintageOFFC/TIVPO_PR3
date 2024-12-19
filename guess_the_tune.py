import pygame


class GuessTheTuneGame:
    def __init__(self, players, tunes):
        if len(players) != 3:
            raise ValueError("Количество игроков должно быть ровно 3.")
        self.players = players
        self.tunes = tunes
        self.current_turn = 0
        self.scores = {player: 0 for player in players}
        self.correct_answers = {}
        self.is_playing = False  # Флаг для контроля воспроизведения

    def play_next_tune(self):
        if self.current_turn >= len(self.tunes):
            raise Exception("Больше нет мелодий для воспроизведения.")
        tune = self.tunes[self.current_turn]
        self.current_turn += 1
        return tune

    def submit_answer(self, player, answer):
        if player not in self.players:
            raise ValueError("Некорректный игрок.")
        if self.current_turn == 0:
            raise Exception("В данный момент мелодия не воспроизводится.")

        last_tune = self.tunes[self.current_turn - 1]
        correct_answer = self.correct_answers.get(last_tune)

        # Приводим оба ответа к одному регистру для независимости от регистра
        if answer.lower() == correct_answer.lower():
            self.scores[player] += 1
            return True
        return False

    def get_winner(self):
        max_score = max(self.scores.values())
        winners = [player for player, score in self.scores.items() if score == max_score]
        return winners[0] if len(winners) == 1 else "Ничья"

    @staticmethod
    def mask_correct_answer(answer):
        """Показывает первую и последнюю буквы, скрывая остальные звёздочками, но не скрывает пробелы."""
        if len(answer) <= 2:
            return answer  # Если ответ состоит из 1-2 символов, ничего не скрываем
        masked = [answer[0]]
        for char in answer[1:-1]:
            if char.isalnum():
                masked.append('*')
            else:
                masked.append(char)
        masked.append(answer[-1])
        return ''.join(masked)

    def play_tune(self, tune):
        """Проигрывает мелодию и управляет флагом is_playing."""
        self.is_playing = True
        try:
            pygame.mixer.init()
            pygame.mixer.music.load("sounds\\" + tune)
            pygame.mixer.music.play()
            while pygame.mixer.music.get_busy() and self.is_playing:
                pygame.time.Clock().tick(10)
        except Exception as e:
            print(f"Ошибка воспроизведения: {e}")
        finally:
            self.is_playing = False

    def stop_tune(self):
        """Прерывает воспроизведение текущей мелодии."""
        self.is_playing = False
        pygame.mixer.music.stop()
