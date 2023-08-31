import numpy as np
from typing import Tuple
from dataclasses import dataclass

@dataclass(frozen=True, eq=False)
class LeagueStats:
    # Total players in this league.
    players: int
    # Average amount of wins per player in the league.
    avg_wins: float
    # Average veterans ratio in this league (veteran=true value in the response).
    avg_veterans_ratio: float
    # Average win-lose ratio per player in the league.
    avg_wl_ratio: float
    # Average League Points per player in the league.
    avg_lp: float
    
class LeaguesDigest:
    def __init__(self):
        # Maximum amount of players, per league.
        self.max_players = 0
        # Highest average of wins, per league.
        self.max_avg_wins = 0
        # Highest average of League Points, per league.
        self.max_avg_lp = 0
    
    def update(self, stats: LeagueStats):
        self.max_players = max(self.max_players, stats.players)
        self.max_avg_wins = max(self.max_avg_wins, stats.avg_wins)
        self.max_avg_lp = max(self.max_avg_lp, stats.avg_lp)
    
    def evaluate_league_score(self, stats: LeagueStats, weights: Tuple[float, float, float, float, float]) -> float:
        return np.average([
            stats.players / self.max_players,
            stats.avg_wins / self.max_avg_wins,
            stats.avg_wl_ratio,
            stats.avg_veterans_ratio,
            stats.avg_lp / self.max_avg_lp,
        ], weights=weights)

@dataclass(frozen=True, eq=False)
class RegionDigest:    
    challenger_stats: LeagueStats
    grandmaster_stats: LeagueStats
    master_stats: LeagueStats

    def evaluate_region_score(self, challenger_digest: LeaguesDigest,
                              grandmaster_digest: LeaguesDigest,
                              master_digest: LeaguesDigest,
                              league_weights: Tuple[float, float, float],
                              league_props_weights: Tuple[float, float, float, float, float]) -> float:
        challenger_score = challenger_digest.evaluate_league_score(self.challenger_stats, league_props_weights)
        grandmaster_score = grandmaster_digest.evaluate_league_score(self.grandmaster_stats, league_props_weights)
        master_score = master_digest.evaluate_league_score(self.master_stats, league_props_weights)
        return np.average([challenger_score, grandmaster_score, master_score], weights=league_weights)
