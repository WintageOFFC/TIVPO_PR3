from behave import given, when, then
from guess_the_tune import GuessTheTuneGame


@given(u'я создаю игру с именами игроков "{player1}", "{player2}", "{player3}"')
def step_create_game(context, player1, player2, player3):
    context.game = GuessTheTuneGame(players=[player1, player2, player3], tunes=[])
    context.players = [player1, player2, player3]


@given(u'список мелодий "{tune1}", "{tune2}", "{tune3}"')
def step_set_tunes(context, tune1, tune2, tune3):
    context.game.tunes = [tune1, tune2, tune3]


@given(u'правильные ответы "{answer1}", "{answer2}", "{answer3}"')
def step_set_correct_answers(context, answer1, answer2, answer3):
    context.game.correct_answers = {
        context.game.tunes[0]: answer1.split(": ")[1],
        context.game.tunes[1]: answer2.split(": ")[1],
        context.game.tunes[2]: answer3.split(": ")[1]
    }


@when(u'игрок "{player}" угадывает мелодию "{tune}" как "{guess}"')
def step_guess_tune(context, player, tune, guess):
    context.game.play_next_tune()
    context.result = context.game.submit_answer(player, guess)


@then(u'счет игрока "{player}" должен быть {expected_score}')
def step_check_score(context, player, expected_score):
    assert context.game.scores[player] == int(expected_score)


@given(u'финальные счета игроков {player1}: {score1}, {player2}: {score2}, {player3}: {score3}')
def step_set_final_scores(context, player1, score1, player2, score2, player3, score3):
    # Устанавливаем финальные счета игроков в контексте игры
    context.game.scores = {
        player1: int(score1),
        player2: int(score2),
        player3: int(score3)
    }


@then(u'победителем должна быть "{winner}"')
def step_check_winner(context, winner):
    assert context.game.get_winner() == winner


@then(u'результат должен быть ничьей между "{players}"')
def step_check_draw(context, players):
    players_list = players.split(" и ")
    player_scores = context.game.scores
    max_score = max(player_scores.values())
    # Проверяем, что игроки с максимальным баллом имеют одинаковые очки
    draw_players = [player for player, score in player_scores.items() if score == max_score]
    assert set(draw_players) == set(players_list), f"Ожидаемые игроки с ничьей: {players_list}, но нашли: {draw_players}"

