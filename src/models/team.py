"""
Team model for cricket simulation.

This module defines the Team class for managing player rosters.
"""

from typing import List, Optional
from .player import Player


class Team:
    """
    Represents a cricket team with player roster management.
    
    Attributes:
        team_id: Unique identifier for the team
        name: Team name
        players: List of players in the team
        captain: Team captain (optional)
        max_players: Maximum number of players allowed (default: 15)
    """
    
    def __init__(
        self,
        team_id: str,
        name: str,
        captain: Optional[Player] = None,
        max_players: int = 15
    ):
        """
        Initialize a new Team.
        
        Args:
            team_id: Unique identifier for the team
            name: Team name
            captain: Team captain (optional)
            max_players: Maximum roster size (default: 15)
        """
        self.team_id = team_id
        self.name = name
        self.captain = captain
        self.max_players = max_players
        self.players: List[Player] = []
    
    def add_player(self, player: Player) -> bool:
        """
        Add a player to the team roster.
        
        Args:
            player: Player to add
            
        Returns:
            True if player was added, False if roster is full
        """
        # For playing XI, limit to 11 players
        playing_xi_limit = 11
        if len(self.players) >= playing_xi_limit:
            return False
        
        self.players.append(player)
        player.team = self.name
        return True
    
    def remove_player(self, player_id: str) -> bool:
        """
        Remove a player from the team roster.
        
        Args:
            player_id: ID of the player to remove
            
        Returns:
            True if player was removed, False if not found
        """
        for i, player in enumerate(self.players):
            if player.player_id == player_id:
                self.players.pop(i)
                return True
        return False
    
    def get_player(self, player_id: str) -> Optional[Player]:
        """
        Get a player by ID.
        
        Args:
            player_id: ID of the player to retrieve
            
        Returns:
            Player object if found, None otherwise
        """
        for player in self.players:
            if player.player_id == player_id:
                return player
        return None
    
    def get_players_by_role(self, role: str) -> List[Player]:
        """
        Get all players with a specific role.
        
        Args:
            role: Player role to filter by
            
        Returns:
            List of players with the specified role
        """
        return [p for p in self.players if p.role == role]
    
    def get_batting_order(self) -> List[Player]:
        """
        Get the batting order for the team.
        
        Returns batsmen first, then all-rounders, then bowlers.
        Wicket-keepers are placed based on their batting strength (usually middle order).
        
        Returns:
            List of players in batting order
        """
        batsmen = [p for p in self.players if p.role == "batsman"]
        wicket_keepers = [p for p in self.players if p.role == "wicket-keeper"]
        all_rounders = [p for p in self.players if p.role == "all-rounder"]
        bowlers = [p for p in self.players if p.role == "bowler"]
        
        # Sort batsmen by average (best first)
        batsmen.sort(key=lambda p: p.batting_stats.average, reverse=True)
        
        # Wicket-keepers typically bat in middle order
        wicket_keepers.sort(key=lambda p: p.batting_stats.average, reverse=True)
        
        # All-rounders in middle order
        all_rounders.sort(key=lambda p: p.batting_stats.average, reverse=True)
        
        # Bowlers at the end (sorted by batting ability)
        bowlers.sort(key=lambda p: p.batting_stats.average, reverse=True)
        
        # Combine: top batsmen, WK, all-rounders, remaining batsmen, bowlers
        batting_order = []
        
        # Add top 2-3 batsmen
        batting_order.extend(batsmen[:3])
        
        # Add wicket-keeper(s) in middle order
        batting_order.extend(wicket_keepers)
        
        # Add all-rounders
        batting_order.extend(all_rounders)
        
        # Add remaining batsmen
        batting_order.extend(batsmen[3:])
        
        # Add bowlers
        batting_order.extend(bowlers)
        
        return batting_order
    
    def get_bowlers(self) -> List[Player]:
        """
        Get all players who can bowl.
        
        Returns bowlers first, then all-rounders.
        
        Returns:
            List of players who can bowl
        """
        bowlers = [p for p in self.players if p.role == "bowler"]
        all_rounders = [p for p in self.players if p.role == "all-rounder"]
        
        # Sort by bowling average (best first)
        bowlers.sort(key=lambda p: p.bowling_stats.average if p.bowling_stats.average > 0 else 999)
        all_rounders.sort(key=lambda p: p.bowling_stats.average if p.bowling_stats.average > 0 else 999)
        
        return bowlers + all_rounders
    
    def set_captain(self, player: Player) -> bool:
        """
        Set the team captain.
        
        Args:
            player: Player to set as captain
            
        Returns:
            True if captain was set, False if player not in team
        """
        if player in self.players:
            self.captain = player
            return True
        return False
    
    def get_roster_count(self) -> int:
        """
        Get the current number of players in the roster.
        
        Returns:
            Number of players
        """
        return len(self.players)
    
    def __repr__(self) -> str:
        """Return string representation of the team."""
        captain_name = self.captain.name if self.captain else "None"
        return f"Team(id={self.team_id}, name={self.name}, players={len(self.players)}, captain={captain_name})"
    
    def get_summary(self) -> str:
        """
        Get a summary of the team.
        
        Returns:
            Formatted string with team details
        """
        summary = f"\n{self.name}\n"
        summary += f"Team ID: {self.team_id}\n"
        summary += f"Captain: {self.captain.name if self.captain else 'TBD'}\n"
        summary += f"Squad Size: {len(self.players)}/{self.max_players}\n"
        summary += f"\nRoster:\n"
        
        for player in self.players:
            summary += f"  - {player.name} ({player.role})\n"
        
        return summary
