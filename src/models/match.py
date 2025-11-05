"""
Match model for cricket simulation.

This module defines the Match class for holding game context.
"""

from typing import Optional, List, Dict, Tuple, Any
from datetime import datetime
from enum import Enum
from .team import Team
from .player import Player


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


class InningsData:
    """Data structure to track innings information."""
    
    def __init__(self):
        self.score: int = 0
        self.wickets: int = 0
        self.overs: int = 0
        self.balls: int = 0
        self.extras: int = 0
        self.batting_scores: Dict[str, int] = {}  # player_id -> runs
        self.batting_balls: Dict[str, int] = {}   # player_id -> balls faced
        self.bowling_figures: Dict[str, Dict[str, int]] = {}  # player_id -> {overs, runs, wickets}
        self.fall_of_wickets: List[Tuple[int, int, str]] = []  # (score, wickets, batsman_name)
        self.partnerships: List[Dict[str, Any]] = []
        self.ball_by_ball: List[Dict[str, Any]] = []
        
    def get_overs_float(self) -> float:
        """Get overs in decimal format (e.g., 19.4 for 19 overs 4 balls)."""
        return self.overs + (self.balls / 10.0)


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
        innings1: First innings data
        innings2: Second innings data
        current_batsman_1: Currently batting (striker)
        current_batsman_2: Currently batting (non-striker)
        current_bowler: Currently bowling
        player_of_match: Player of the match
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
        
        # Innings tracking
        self.innings1 = InningsData()
        self.innings2 = InningsData()
        
        # Current match state
        self.current_batsman_1: Optional[Player] = None
        self.current_batsman_2: Optional[Player] = None
        self.current_bowler: Optional[Player] = None
        self.player_of_match: Optional[Player] = None
        
        # Legacy fields for compatibility
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
    
    def generate_scorecard(self) -> str:
        """
        Generate a detailed scorecard for the match.
        
        Returns:
            Formatted scorecard string
        """
        scorecard = "\n" + "="*70 + "\n"
        scorecard += f"{'MATCH SCORECARD':^70}\n"
        scorecard += "="*70 + "\n"
        scorecard += f"{self.team_a.name} vs {self.team_b.name}\n"
        scorecard += f"Format: {self.format.value} | Venue: {self.venue}\n"
        scorecard += "="*70 + "\n\n"
        
        if self.toss_winner:
            scorecard += f"Toss: {self.toss_winner.name} won and elected to {self.elected_to}\n\n"
        
        # First Innings
        scorecard += f"{self.team_a.name} Innings\n"
        scorecard += "-"*70 + "\n"
        scorecard += f"Score: {self.innings1.score}/{self.innings1.wickets} "
        scorecard += f"({self.innings1.overs}.{self.innings1.balls} overs)\n"
        
        if self.innings1.batting_scores:
            scorecard += "\nBatting:\n"
            scorecard += f"{'Player':<25} {'Runs':<10} {'Balls':<10}\n"
            scorecard += "-"*70 + "\n"
            for player_id, runs in sorted(self.innings1.batting_scores.items(), 
                                         key=lambda x: x[1], reverse=True):
                balls = self.innings1.batting_balls.get(player_id, 0)
                scorecard += f"{player_id:<25} {runs:<10} {balls:<10}\n"
        
        if self.innings1.bowling_figures:
            scorecard += "\nBowling:\n"
            scorecard += f"{'Player':<25} {'Overs':<10} {'Runs':<10} {'Wickets':<10}\n"
            scorecard += "-"*70 + "\n"
            for player_id, figures in self.innings1.bowling_figures.items():
                overs = figures.get('overs', 0)
                runs = figures.get('runs', 0)
                wickets = figures.get('wickets', 0)
                scorecard += f"{player_id:<25} {overs:<10} {runs:<10} {wickets:<10}\n"
        
        scorecard += "\n" + "="*70 + "\n\n"
        
        # Second Innings (if exists)
        if self.innings2.score > 0 or self.innings2.wickets > 0:
            scorecard += f"{self.team_b.name} Innings\n"
            scorecard += "-"*70 + "\n"
            scorecard += f"Score: {self.innings2.score}/{self.innings2.wickets} "
            scorecard += f"({self.innings2.overs}.{self.innings2.balls} overs)\n"
            
            if self.innings2.batting_scores:
                scorecard += "\nBatting:\n"
                scorecard += f"{'Player':<25} {'Runs':<10} {'Balls':<10}\n"
                scorecard += "-"*70 + "\n"
                for player_id, runs in sorted(self.innings2.batting_scores.items(), 
                                             key=lambda x: x[1], reverse=True):
                    balls = self.innings2.batting_balls.get(player_id, 0)
                    scorecard += f"{player_id:<25} {runs:<10} {balls:<10}\n"
            
            if self.innings2.bowling_figures:
                scorecard += "\nBowling:\n"
                scorecard += f"{'Player':<25} {'Overs':<10} {'Runs':<10} {'Wickets':<10}\n"
                scorecard += "-"*70 + "\n"
                for player_id, figures in self.innings2.bowling_figures.items():
                    overs = figures.get('overs', 0)
                    runs = figures.get('runs', 0)
                    wickets = figures.get('wickets', 0)
                    scorecard += f"{player_id:<25} {overs:<10} {runs:<10} {wickets:<10}\n"
            
            scorecard += "\n" + "="*70 + "\n"
        
        # Match Result
        if self.status == MatchStatus.COMPLETED:
            scorecard += f"\nResult: {self.result_text}\n"
            if self.player_of_match:
                scorecard += f"Player of the Match: {self.player_of_match.name}\n"
        
        scorecard += "="*70 + "\n"
        
        return scorecard
    
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
