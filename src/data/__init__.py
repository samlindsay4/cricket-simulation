"""
Data loading and processing utilities.

This module handles loading player and team data from files.
"""

from .data_loader import (
    load_teams_from_json,
    get_default_teams,
    get_team_by_name,
    list_available_teams
)

__all__ = [
    'load_teams_from_json',
    'get_default_teams',
    'get_team_by_name',
    'list_available_teams'
]
