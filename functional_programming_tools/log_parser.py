# -*- coding: utf-8 -*-


PROCESSED_FILE = "events.txt"


def grouped_events(file_name):
    sign_time = 17
    stat_nok = {}
    with open(file_name, mode='r') as file:
        current_time = None
        for line in file:
            if line[1:sign_time] != current_time:
                if current_time and stat_nok[current_time]:
                    yield current_time, stat_nok[current_time]
                current_time = line[1:sign_time]
                stat_nok[current_time] = 0
            if line.endswith('NOK\n'):
                stat_nok[current_time] += 1
        if current_time and stat_nok[current_time]:
            yield current_time, stat_nok[current_time]


grouped_events = grouped_events(PROCESSED_FILE)
for group_time, event_count in grouped_events:
    print(f'[{group_time}] {event_count}')
