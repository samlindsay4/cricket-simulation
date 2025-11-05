"""
Data loading utilities for cricket simulation.

This module handles loading team and player data from JSON files.
"""

import json
import os
from typing import List, Dict, Any
from ..models.player import Player
from ..models.team import Team


def load_teams_from_json(filepath: str) -> List[Team]:
    """
    Load teams and players from a JSON file.
    
    Args:
        filepath: Path to the JSON file containing team data
    
    Returns:
        List of Team objects with players
    
    Raises:
        FileNotFoundError: If the JSON file doesn't exist
        ValueError: If the JSON format is invalid
    """
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"Team data file not found: {filepath}")
    
    with open(filepath, 'r') as f:
        data = json.load(f)
    
    teams = []
    
    for team_data in data.get('teams', []):
        team = Team(
            team_id=team_data['id'],
            name=team_data['name']
        )
        
        for player_data in team_data.get('players', []):
            player = Player(
                player_id=player_data['id'],
                name=player_data['name'],
                team=team.name,
                role=player_data['role'],
                country=team_data.get('country', 'Unknown'),
                batting_average=player_data.get('batting_average', 30.0),
                strike_rate=player_data.get('strike_rate', 100.0),
                centuries=player_data.get('centuries', 0),
                fifties=player_data.get('fifties', 0),
                bowling_average=player_data.get('bowling_average', 30.0),
                economy_rate=player_data.get('economy_rate', 6.0),
                wickets_taken=player_data.get('wickets_taken', 0),
                bowling_strike_rate=player_data.get('bowling_strike_rate', 30.0)
            )
            team.add_player(player)
        
        teams.append(team)
    
    return teams


def get_default_teams() -> List[Team]:
    """
    Get the default sample teams.
    
    Loads teams from the default sample_teams.json file.
    
    Returns:
        List of Team objects with players
    """
    # Get the path to sample_teams.json relative to this file
    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(os.path.dirname(current_dir))
    filepath = os.path.join(project_root, 'data', 'sample_teams.json')
    
    return load_teams_from_json(filepath)


def get_team_by_name(teams: List[Team], name: str) -> Team:
    """
    Get a team by name from a list of teams.
    
    Args:
        teams: List of teams to search
        name: Name of the team to find
    
    Returns:
        Team object
    
    Raises:
        ValueError: If team not found
    """
    for team in teams:
        if team.name.lower() == name.lower():
            return team
    
    raise ValueError(f"Team '{name}' not found")


def list_available_teams(teams: List[Team]) -> List[str]:
    """
    Get a list of available team names.
    
    Args:
        teams: List of teams
    
    Returns:
        List of team names
    """
    return [team.name for team in teams]
