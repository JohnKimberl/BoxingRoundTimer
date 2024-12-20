#!/usr/bin/env python3

import sh
import sys
import time
import random
import bisect
import argparse

COMBINATIONS = {
    '1 2': 5.0,
    '1 2 3': 4.5,
    '1 1 2 3': 4.0,
    '1 2 3 2': 4.2,
    '1 1 2': 3.5,
    '1 1 2 down 2': 3.5,
    '1 2 down 2': 3.5,
    '1 2 3 3': 3.2,
    '1 2 back 2': 2.2,
    '1 2 body body': 2.0,
    '1 2 3 4': 2.0,
    '1 2 1 2': 1.5,
    '2 3 2': 1.0,
}

def play_sound(words, rate=220):
    sh.say(words, '-r %d' % rate)

def select_combo():
    items = list(COMBINATIONS.keys())  # Convert to list for compatibility
    mysum = 0
    breakpoints = []
    for i in items:
        mysum += COMBINATIONS[i]
        breakpoints.append(mysum)
    score = random.random() * breakpoints[-1]
    return items[bisect.bisect(breakpoints, score)]

def play_combo():
    play_sound(select_combo())

def get_seconds_since_epoch():
    return time.mktime(time.gmtime())

def do_round(round_number, length=3):
    print(f'Round {round_number}')
    play_sound(f'Round {round_number}', 200)
    time.sleep(1.5)
    length_in_seconds = length * 60.0
    start = get_seconds_since_epoch()
    while length_in_seconds >= (get_seconds_since_epoch() - start):
        try:
            play_combo()
            time.sleep(1.8)
        except KeyboardInterrupt:
            print('Ending it early huh? Pffft bitch made.')
            sys.exit(0)

    print(f'Round {round_number} COMPLETE\n\n')
    play_sound(f'Round {round_number} complete', 200)

def run_drill(number_of_rounds, round_length, rest_period=60):
    for round_number in range(1, number_of_rounds + 1):
        do_round(round_number, round_length)
        time.sleep(rest_period)
        print('10 seconds')
        play_sound('10 seconds')
        time.sleep(10)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Drill runner for combinations')
    parser.add_argument('-r', '--rounds', required=True, type=int, dest='number_of_rounds',
                        help='Number of rounds')
    parser.add_argument('-l', '--round_length', default=3, type=int, dest='round_length',
                        help='Length of each round in minutes. Default 3 minutes.')
    args = parser.parse_args()
    run_drill(args.number_of_rounds, args.round_length)
