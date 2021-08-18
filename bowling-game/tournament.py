# -*- coding: utf-8 -*-


import argparse

from bowling import Game
import logging

result_errors_log = logging.getLogger('main')
result_errors_log.setLevel(logging.ERROR)
result_errors_fh = logging.FileHandler('bowling_errors.log', 'w', 'utf8')
result_errors_formatter = logging.Formatter('%(levelname)s - %(message)s')
result_errors_fh.setFormatter(result_errors_formatter)
result_errors_log.addHandler(result_errors_fh)


def process_game_result(input_file, output_file, production):
    with open(output_file, mode='w', encoding='utf8') as output:
        with open(input_file, mode='r', encoding='utf8') as file:
            new_tour_gamers_list = []
            participants = {}
            """
            participants = {
                gamer_name = [number_of_matches, number_of_wins],
                .....
            }
            """

            for new_line in file:
                new_line = new_line[:-1]
                if 'Tour' in new_line:
                    number_of_tour = new_line.split()[-1]
                    output.write(f'Тур\t{number_of_tour}\n')
                    new_tour_gamers_list = []
                elif 'winner' in new_line:
                    max_score = max([gamer[1] for gamer in new_tour_gamers_list]) \
                        if new_tour_gamers_list else None
                    potential_winners = [gamer for gamer in new_tour_gamers_list if gamer[1] == max_score]
                    if len(potential_winners) > 1:
                        winner = 'ничья'
                    elif potential_winners:
                        winner = potential_winners[0][0]
                        participants[winner][1] += 1
                    else:
                        winner = '-------'
                    output.write(f'winner\t\t{winner:*^12}\n')
                elif new_line:
                    gamer_tour_inf = new_line.split('\t')
                    gamer_name = gamer_tour_inf[0]
                    gamer_result = gamer_tour_inf[1]
                    participants.setdefault(gamer_name, [0, 0])
                    participants[gamer_name][0] += 1
                    try:
                        gamer_score = Game(production).go(gamer_result)
                        new_tour_gamers_list.append((gamer_name, gamer_score))
                        output.write(f'{gamer_name:12}{gamer_result:25}{gamer_score:5}\n')
                    except Exception as exc:
                        result_errors_log.error(f'Тур{number_of_tour} {new_line} {exc}')
                else:
                    output.write('\n')

            print_player_rating(participants)


def print_player_rating(participants):
    participants_list = list(participants.items())
    participants_list.sort(key=lambda x: x[1][0])
    participants_list.sort(key=lambda x: x[1][1], reverse=True)
    print('+----------+------------------+--------------+')
    print('| Игрок    |  сыграно матчей  |  всего побед |')
    print('+----------+------------------+--------------+')
    for gamer in participants_list:
        print(f'+{gamer[0]:^10}|{gamer[1][0]:^18}|{gamer[1][1]:^14}|')
        print('+----------+------------------+--------------+')


if __name__ == '__main__':
    console_parser = argparse.ArgumentParser(description='Результаты турнира')
    console_parser.add_argument('-in', '--input', dest='input_file', type=str)
    console_parser.add_argument('-out', '--output', dest='output_file', type=str)
    console_parser.add_argument('-pd', '--product', dest='production', action='store_const', const=True, default=False)
    args = console_parser.parse_args()
    INPUT_FILE = args.input_file
    OUTPUT_FILE = args.output_file
    production = args.production

    process_game_result(INPUT_FILE, OUTPUT_FILE, production=production)

INPUT_FILE = 'tournament.txt'
OUTPUT_FILE = 'bowling_result.txt'
