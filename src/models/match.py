"""
Match model for cricket simulation.

This module defines the Match class for holding game context.
"""

from typing import Optional, List
from datetime import datetime
from enum import Enum
from .team import Team


class MatchFormat(Enum):
    """Cricket match formats."""
    
    T20 = "T20"
    ODI = "ODI"
    TEST = "Test"


class MatchStatus(Enum):
    """Match status."""
    
    NOT_STARTED = "Not Started"
    IN_PROGRESS = "In Progress"
    COMPLETED = "Completed"
    ABANDONED = "Abandoned"


class Match:
    """
    Represents a cricket match between two teams.
    
    Attributes:
        match_id: Unique identifier for the match
        team_a: First team
        team_b: Second team
        format: Match format (T20, ODI, or Test)
        venue: Match venue
        date: Match date
        toss_winner: Team that won the toss (optional)
        elected_to: What the toss winner elected to do (bat/bowl)
        status: Current match status
        winner: Winning team (optional)
        result_text: Description of match result
    """
    
    def __init__(
        self,
        match_id: str,
        team_a: Team,
        team_b: Team,
        format: MatchFormat = MatchFormat.T20,
        venue: str = "TBD",
        date: Optional[datetime] = None
    ):
        """
        Initialize a new Match.
        
        Args:
            match_id: Unique identifier for the match
            team_a: First team
            team_b: Second team
            format: Match format (default: T20)
            venue: Match venue (default: "TBD")
            date: Match date (default: current datetime)
        """
        self.match_id = match_id
        self.team_a = team_a
        self.team_b = team_b
        self.format = format
        self.venue = venue
        self.date = date or datetime.now()
        
        self.toss_winner: Optional[Team] = None
        self.elected_to: Optional[str] = None
        self.status = MatchStatus.NOT_STARTED
        self.winner: Optional[Team] = None
        self.result_text: str = ""
        
        # These will be populated during simulation
        self.team_a_score: int = 0
        self.team_a_wickets: int = 0
        self.team_a_overs: float = 0.0
        
        self.team_b_score: int = 0
        self.team_b_wickets: int = 0
        self.team_b_overs: float = 0.0
    
    def conduct_toss(self, winning_team: Team, elected_to: str) -> None:
        """
        Record the toss result.
        
        Args:
            winning_team: Team that won the toss
            elected_to: Choice made by toss winner ("bat" or "bowl")
        """
        if winning_team not in [self.team_a, self.team_b]:
            raise ValueError("Toss winner must be one of the competing teams")
        
        if elected_to not in ["bat", "bowl"]:
            raise ValueError("Elected choice must be 'bat' or 'bowl'")
        
        self.toss_winner = winning_team
        self.elected_to = elected_to
    
    def start_match(self) -> None:
        """Mark the match as started."""
        if self.status == MatchStatus.NOT_STARTED:
            self.status = MatchStatus.IN_PROGRESS
    
    def end_match(self, winner: Optional[Team], result_text: str) -> None:
        """
        End the match and record the result.
        
        Args:
            winner: Winning team (None for draw/tie)
            result_text: Description of the result
        """
        if winner and winner not in [self.team_a, self.team_b]:
            raise ValueError("Winner must be one of the competing teams or None")
        
        self.winner = winner
        self.result_text = result_text
        self.status = MatchStatus.COMPLETED
    
    def get_max_overs(self) -> int:
        """
        Get maximum overs per innings based on format.
        
        Returns:
            Maximum overs for the match format
        """
        if self.format == MatchFormat.T20:
            return 20
        elif self.format == MatchFormat.ODI:
            return 50
        else:  # Test
            return 90  # Typical day's play
    
    def __repr__(self) -> str:
        """Return string representation of the match."""
        return (f"Match(id={self.match_id}, {self.team_a.name} vs {self.team_b.name}, "
                f"format={self.format.value}, status={self.status.value})")
    
    def get_summary(self) -> str:
        """
        Get a summary of the match.
        
        Returns:
            Formatted string with match details
        """
        summary = f"\n{'='*50}\n"
        summary += f"{self.team_a.name} vs {self.team_b.name}\n"
        summary += f"Format: {self.format.value}\n"
        summary += f"Venue: {self.venue}\n"
        summary += f"Date: {self.date.strftime('%Y-%m-%d')}\n"
        summary += f"Status: {self.status.value}\n"
        
        if self.toss_winner:
            summary += f"\nToss: {self.toss_winner.name} won and elected to {self.elected_to}\n"
        
        if self.status != MatchStatus.NOT_STARTED:
            summary += f"\nScorecard:\n"
            summary += f"{self.team_a.name}: {self.team_a_score}/{self.team_a_wickets} ({self.team_a_overs} overs)\n"
            summary += f"{self.team_b.name}: {self.team_b_score}/{self.team_b_wickets} ({self.team_b_overs} overs)\n"
        
        if self.status == MatchStatus.COMPLETED:
            summary += f"\nResult: {self.result_text}\n"
        
        summary += f"{'='*50}\n"
        return summary
