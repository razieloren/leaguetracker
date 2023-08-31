import numpy as np
from typing import Dict, Tuple, List

from riot.api import API
from riot.modules.consts import Queue, Region

from .stats import LeagueStats, RegionDigest, LeaguesDigest

def get_league_stats(entries) -> LeagueStats:
    total_wins = 0
    total_veterans = 0
    total_wl_ratio = 0
    total_league_points = 0
    for entry in entries:
        total_wins += entry.wins
        if entry.veteran:
            total_veterans += 1
        total_wl_ratio += (entry.wins / (entry.wins + entry.losses))
        total_league_points += entry.leaguePoints
    return LeagueStats(
        len(entries),
        total_wins / len(entries),
        total_veterans / len(entries),
        total_wl_ratio / len(entries),
        total_league_points / len(entries)
    )

def get_region_digest(api: API) -> RegionDigest:
    challenger_stats = get_league_stats(
        api.league.get_challenger_league(Queue.RankedSolo).entries)
    grandmaster_stats = get_league_stats(
        api.league.get_grand_master_league(Queue.RankedSolo).entries)
    master_stats = get_league_stats(
        api.league.get_master_league(Queue.RankedSolo).entries)
    return RegionDigest(challenger_stats, grandmaster_stats, master_stats)

class LeagueTracker:
    _REGIONS_TO_TRACK = [Region.BRAZIL, Region.EUNE, Region.EUW, Region.JP, Region.KR, Region.LATIN1, Region.LATIN2, Region.NA, Region.OC, Region.TR, Region.RU, Region.PH, Region.SG, Region.TH, Region.TW, Region.VN]

    def __init__(self):
        self._challenger_digest = LeaguesDigest()
        self._grandmaster_digest = LeaguesDigest()
        self._master_digest = LeaguesDigest()
        self._region_digests: Dict[Region, RegionDigest] = {}
        self._region_acc_scores: Dict[Region, List[Tuple[int, float]]] = {}
        for region in self._REGIONS_TO_TRACK:
            self._region_acc_scores[region] = []

    def load_data(self, api_key: str):
        for region in self._REGIONS_TO_TRACK:
            api = API(region, api_key)
            region_digest = get_region_digest(api)
            self._challenger_digest.update(region_digest.challenger_stats)
            self._grandmaster_digest.update(region_digest.grandmaster_stats)
            self._master_digest.update(region_digest.master_stats)
            self._region_digests[region] = region_digest

    def evaluate_regions(self,
                         league_weights: Tuple[float, float, float],
                         league_props_weights: Tuple[float, float, float, float, float]) -> List[Tuple[Region, float]]:
        region_scores: List[Tuple[Region, float]] = []
        for region, region_digest in self._region_digests.items():
            region_scores.append((region, region_digest.evaluate_region_score(
                self._challenger_digest,
                self._grandmaster_digest,
                self._master_digest,
                league_weights,
                league_props_weights
            )))
        return sorted(region_scores, key=lambda x: x[1], reverse=True)
    
    def evaluate_and_acc_regions(self,
                            league_weights: Tuple[float, float, float],
                            league_props_weights: Tuple[float, float, float, float, float]) -> List[Tuple[Region, float]]:
        scores = self.evaluate_regions(league_weights, league_props_weights)
        for rank, evaluation in enumerate(scores):
            region, score = evaluation
            self._region_acc_scores[region].append((rank + 1, score))

    def sorted_region_acc_by_avg_rank(self) -> List[Tuple[Region, float, float]]:
        acc_list: List[Tuple[Region, float, float]] = []
        for region, acc in self._region_acc_scores.items():
            avg_rank = np.average(list(map(lambda x: x[0], acc)))
            avg_score = np.average(list(map(lambda x: x[1], acc)))
            acc_list.append((
                region,
                avg_rank,
                avg_score
            ))
        return sorted(acc_list, key=lambda x: x[1])

