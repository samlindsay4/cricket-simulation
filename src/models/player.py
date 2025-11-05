"""
Player model for cricket simulation.

This module defines the Player class with batting, bowling, and fielding statistics.
"""

from typing import Optional
from dataclasses import dataclass, field


@dataclass
class BattingStats:
    """Player batting statistics."""
    
    matches: int = 0
    innings: int = 0
    runs: int = 0
    highest_score: int = 0
    average: float = 0.0
    strike_rate: float = 0.0
    centuries: int = 0
    half_centuries: int = 0
    fours: int = 0
    sixes: int = 0
    
    def update_average(self, not_outs: int = 0) -> None:
        """Calculate and update batting average."""
        if self.innings - not_outs > 0:
            self.average = self.runs / (self.innings - not_outs)
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
            self.strike_rate = (self.overs * 6) / self.wickets if self.wickets > 0 else 0.0
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
        batting_stats: Player's batting statistics
        bowling_stats: Player's bowling statistics
        fielding_stats: Player's fielding statistics
    """
    
    def __init__(
        self,
        player_id: str,
        name: str,
        team: Optional[str] = None,
        role: str = "batsman"
    ):
        """
        Initialize a new Player.
        
        Args:
            player_id: Unique identifier for the player
            name: Player's full name
            team: Team the player belongs to (optional)
            role: Player's role - one of: batsman, bowler, all-rounder, wicket-keeper
        """
        self.player_id = player_id
        self.name = name
        self.team = team
        self.role = role
        
        self.batting_stats = BattingStats()
        self.bowling_stats = BowlingStats()
        self.fielding_stats = FieldingStats()
    
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
