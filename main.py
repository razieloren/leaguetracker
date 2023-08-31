#!/usr/bin/env python3

import argparse
import tabulate

from itertools import product, permutations
from league_tracker.league_tracker import LeagueTracker

# Challenger, Grandmaster, Master
LEAGUE_WEIGHTS = \
    [(1, 1, 1)] + \
    list(permutations([1, 2, 4])) + \
    list(permutations([1, 2, 100]))

# Number of players, Wins, WL Ratio, Veterans Ratio, LP
LEAGUE_PROPS_WEIGHTS = \
    [(1, 1, 1, 1, 1)] + \
    list(permutations([1, 2, 3, 4, 5])) + \
    list(permutations([1, 2, 4, 8, 16])) + \
    list(permutations([1, 2, 4, 8, 100]))

def parse_args() -> argparse.Namespace:
    args = argparse.ArgumentParser(description='LeagueTracker')
    args.add_argument('-k', '--api-key', help='Riot API key', required=True)
    return args.parse_args()

def main():
    args = parse_args()
    tracker = LeagueTracker()
    tracker.load_data(args.api_key)
    for league_weights, league_props_weights in product(LEAGUE_WEIGHTS, LEAGUE_PROPS_WEIGHTS):
        tracker.evaluate_and_acc_regions(league_weights, league_props_weights)
    acc_regions = tracker.sorted_region_acc_by_avg_rank()
    print(tabulate.tabulate(
        map(lambda region: (region[0].value.friendly_name, region[1], region[2]), acc_regions),
        headers=['Region', 'Average Rank', 'Average Score']))


if __name__ == '__main__':
    main()