import unittest
from unittest.mock import patch
from guess_the_tune import GuessTheTuneGame


class TestGuessTheTune(unittest.TestCase):
    def test_game_initialization(self):
        game = GuessTheTuneGame(players=['Алиса', 'Борис', 'Катя'], tunes=['Мелодия1', 'Мелодия2'])
        self.assertEqual(game.players, ['Алиса', 'Борис', 'Катя'])
        self.assertEqual(game.tunes, ['Мелодия1', 'Мелодия2'])
        self.assertEqual(game.current_turn, 0)
        self.assertEqual(game.scores, {'Алиса': 0, 'Борис': 0, 'Катя': 0})

    def test_invalid_player_count(self):
        with self.assertRaises(ValueError):
            GuessTheTuneGame(players=['Алиса', 'Борис'], tunes=['Мелодия1', 'Мелодия2'])

        with self.assertRaises(ValueError):
            GuessTheTuneGame(players=['Алиса', 'Борис', 'Катя', 'Дима'], tunes=['Мелодия1', 'Мелодия2'])

    def test_play_next_tune(self):
        game = GuessTheTuneGame(players=['Алиса', 'Борис', 'Катя'], tunes=['Мелодия1', 'Мелодия2'])
        self.assertEqual(game.play_next_tune(), 'Мелодия1')
        self.assertEqual(game.current_turn, 1)
        self.assertEqual(game.play_next_tune(), 'Мелодия2')
        self.assertEqual(game.current_turn, 2)

    def test_submit_answer(self):
        game = GuessTheTuneGame(players=['Алиса', 'Борис', 'Катя'], tunes=['Мелодия1'])
        game.correct_answers = {'Мелодия1': 'Песня А'}

        game.play_next_tune()
        self.assertTrue(game.submit_answer('Алиса', 'Песня А'))
        self.assertEqual(game.scores['Алиса'], 1)

        self.assertFalse(game.submit_answer('Борис', 'Неверный ответ'))
        self.assertEqual(game.scores['Борис'], 0)

    def test_game_winner(self):
        game = GuessTheTuneGame(players=['Алиса', 'Борис', 'Катя'], tunes=['Мелодия1'])
        game.scores = {'Алиса': 3, 'Борис': 2, 'Катя': 1}
        self.assertEqual(game.get_winner(), 'Алиса')

    def test_mask_correct_answer(self):
        game = GuessTheTuneGame(players=['Алиса', 'Борис', 'Катя'], tunes=['Мелодия1'])
        self.assertEqual(game.mask_correct_answer('Песня А'), 'П**** А')
        self.assertEqual(game.mask_correct_answer('Песня Б'), 'П**** Б')
        self.assertEqual(game.mask_correct_answer('Б'), 'Б')
        self.assertEqual(game.mask_correct_answer('П'), 'П')
        self.assertEqual(game.mask_correct_answer('П п'), 'П п')

    @patch('pygame.mixer.music.load')
    @patch('pygame.mixer.music.play')
    def test_play_tune(self, mock_play, mock_load):
        game = GuessTheTuneGame(players=['Алиса', 'Борис', 'Катя'], tunes=['song1.mp3'])

        # Проверим, что воспроизведение мелодии происходит корректно
        game.play_tune('song1.mp3')
        mock_load.assert_called_with('sounds\\song1.mp3')
        mock_play.assert_called()

    @patch('pygame.mixer.music.stop')
    def test_stop_tune(self, mock_stop):
        game = GuessTheTuneGame(players=['Алиса', 'Борис', 'Катя'], tunes=['song1.mp3'])

        # Останавливаем музыку и проверяем, что метод stop был вызван
        game.stop_tune()
        mock_stop.assert_called()


if __name__ == '__main__':
    unittest.main()  # verbosity=2
