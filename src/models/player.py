"""
Player model for cricket simulation.

This module defines the Player class with batting, bowling, and fielding statistics.
"""

from typing import Optional
from dataclasses import dataclass, field
import random


@dataclass
class BattingStats:
    """Player batting statistics."""
    
    matches: int = 0
    innings: int = 0
    runs: int = 0
    not_outs: int = 0
    highest_score: int = 0
    average: float = 0.0
    strike_rate: float = 0.0
    centuries: int = 0
    half_centuries: int = 0
    fours: int = 0
    sixes: int = 0
    
    def update_average(self) -> None:
        """Calculate and update batting average."""
        if self.innings - self.not_outs > 0:
            self.average = self.runs / (self.innings - self.not_outs)
        else:
            self.average = 0.0


@dataclass
class BowlingStats:
    """Player bowling statistics."""
    
    matches: int = 0
    innings: int = 0
    overs: float = 0.0
    runs_conceded: int = 0
    wickets: int = 0
    best_figures: str = "0/0"
    average: float = 0.0
    economy: float = 0.0
    strike_rate: float = 0.0
    five_wickets: int = 0
    
    def update_stats(self) -> None:
        """Calculate and update bowling statistics."""
        if self.wickets > 0:
            self.average = self.runs_conceded / self.wickets
            self.strike_rate = (self.overs * 6) / self.wickets
        else:
            self.average = 0.0
            self.strike_rate = 0.0
        
        if self.overs > 0:
            self.economy = self.runs_conceded / self.overs
        else:
            self.economy = 0.0


@dataclass
class FieldingStats:
    """Player fielding statistics."""
    
    matches: int = 0
    catches: int = 0
    stumpings: int = 0
    run_outs: int = 0


class Player:
    """
    Represents a cricket player with comprehensive statistics.
    
    Attributes:
        player_id: Unique identifier for the player
        name: Player's full name
        team: Team the player belongs to
        role: Player's role (batsman, bowler, all-rounder, wicket-keeper)
        country: Player's country
        batting_stats: Player's batting statistics
        bowling_stats: Player's bowling statistics
        fielding_stats: Player's fielding statistics
    """
    
    def __init__(
        self,
        player_id: str,
        name: str,
        team: Optional[str] = None,
        role: str = "batsman",
        country: str = "Unknown",
        batting_average: float = 30.0,
        strike_rate: float = 100.0,
        centuries: int = 0,
        fifties: int = 0,
        bowling_average: float = 30.0,
        economy_rate: float = 6.0,
        wickets_taken: int = 0,
        bowling_strike_rate: float = 30.0
    ):
        """
        Initialize a new Player.
        
        Args:
            player_id: Unique identifier for the player
            name: Player's full name
            team: Team the player belongs to (optional)
            role: Player's role - one of: batsman, bowler, all-rounder, wicket-keeper
            country: Player's country
            batting_average: Career batting average
            strike_rate: Career strike rate
            centuries: Number of centuries scored
            fifties: Number of fifties scored
            bowling_average: Career bowling average
            economy_rate: Career economy rate
            wickets_taken: Total wickets taken
            bowling_strike_rate: Career bowling strike rate
        """
        self.player_id = player_id
        self.name = name
        self.team = team
        self.role = role
        self.country = country
        
        self.batting_stats = BattingStats()
        self.bowling_stats = BowlingStats()
        self.fielding_stats = FieldingStats()
        
        # Set career stats for simulation
        self.batting_stats.average = batting_average
        self.batting_stats.strike_rate = strike_rate
        self.batting_stats.centuries = centuries
        self.batting_stats.half_centuries = fifties
        
        self.bowling_stats.average = bowling_average
        self.bowling_stats.economy = economy_rate
        self.bowling_stats.wickets = wickets_taken
        self.bowling_stats.strike_rate = bowling_strike_rate
    
    def calculate_dismissal_probability(self, bowler: Optional['Player'] = None) -> float:
        """
        Calculate the probability of getting dismissed on this ball.
        
        Uses batsman's average and bowler's average to determine dismissal chance.
        Base rate is ~2-3% per ball, adjusted by player stats.
        
        Args:
            bowler: The bowler bowling this ball (optional)
        
        Returns:
            Probability of dismissal (0.0 to 1.0)
        """
        # Base dismissal probability (about 2.5% per ball)
        base_prob = 0.025
        
        # Better average = lower dismissal chance
        # Average 50 = 0.8x base, Average 25 = 1.2x base
        batting_factor = 37.5 / max(self.batting_stats.average, 15.0)
        
        # If bowler stats available, factor them in
        bowler_factor = 1.0
        if bowler and bowler.bowling_stats.average > 0:
            # Better bowler (lower average) = higher dismissal chance
            # Bowling avg 25 = 1.2x, Bowling avg 35 = 0.8x
            bowler_factor = 30.0 / max(bowler.bowling_stats.average, 20.0)
        
        # Combined probability
        prob = base_prob * batting_factor * bowler_factor
        
        # Cap between 0.5% and 8%
        return max(0.005, min(0.08, prob))
    
    def calculate_scoring_probabilities(self, bowler: Optional['Player'] = None) -> dict:
        """
        Calculate probabilities for different run outcomes.
        
        Uses batsman's strike rate and bowler's economy to determine run distribution.
        
        Args:
            bowler: The bowler bowling this ball (optional)
        
        Returns:
            Dictionary with probabilities for each outcome (0, 1, 2, 3, 4, 6 runs)
        """
        # Base strike rate determines aggression
        sr = self.batting_stats.strike_rate
        
        # Bowler's economy affects scoring difficulty
        economy_factor = 1.0
        if bowler and bowler.bowling_stats.economy > 0:
            # Higher economy = easier scoring
            economy_factor = bowler.bowling_stats.economy / 6.0
        
        # Adjust for strike rate
        # SR 80 = defensive, SR 140 = aggressive
        aggression = (sr / 100.0) * economy_factor
        
        # Base probabilities for different outcomes
        # Dots should be ~40-50% of deliveries
        dot_prob = max(0.35, 0.55 - (aggression * 0.15))
        
        # Singles are most common scoring shot
        single_prob = 0.30
        
        # Twos depend on running ability
        two_prob = 0.10
        
        # Threes are rare
        three_prob = 0.02
        
        # Boundaries based on aggression
        four_prob = min(0.15, 0.05 + (aggression * 0.08))
        six_prob = min(0.10, 0.02 + (aggression * 0.06))
        
        # Normalize to ensure they sum to 1.0
        total = dot_prob + single_prob + two_prob + three_prob + four_prob + six_prob
        
        return {
            0: dot_prob / total,
            1: single_prob / total,
            2: two_prob / total,
            3: three_prob / total,
            4: four_prob / total,
            6: six_prob / total
        }
    
    def __repr__(self) -> str:
        """Return string representation of the player."""
        return f"Player(id={self.player_id}, name={self.name}, team={self.team}, role={self.role})"
    
    def get_summary(self) -> str:
        """
        Get a summary of player statistics.
        
        Returns:
            Formatted string with player statistics
        """
        summary = f"\n{self.name} ({self.role})\n"
        summary += f"Team: {self.team or 'N/A'}\n"
        summary += f"\nBatting: {self.batting_stats.runs} runs @ {self.batting_stats.average:.2f}\n"
        summary += f"Bowling: {self.bowling_stats.wickets} wickets @ {self.bowling_stats.average:.2f}\n"
        summary += f"Fielding: {self.fielding_stats.catches} catches\n"
        return summary
