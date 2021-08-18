# -*- coding: utf-8 -*-


from bowling import Game
import argparse

if __name__ == '__main__':
    consol_parser = argparse.ArgumentParser(description='Расчёт результатов игры')
    consol_parser.add_argument('--score', dest='Game_result', type=str)
    args = consol_parser.parse_args()
    game_result = args.Game_result
    if not game_result:
        game_result = input('введите результат\n')
    game = Game()
    game_score = game.go(game_result)
    print(f'Количество очков для результата {game_result} равно {game_score}')
