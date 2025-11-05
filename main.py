#!/usr/bin/env python3
"""
Cricket Simulation Game - Main Entry Point

A cricket simulation game that allows users to create teams, players,
and simulate cricket matches.
"""

import sys
from typing import Optional
from src.models import Player, Team, Match
from src.models.match import MatchFormat


class CricketSimulationCLI:
    """Command-line interface for the cricket simulation game."""
    
    def __init__(self):
        """Initialize the CLI application."""
        self.teams = {}
        self.players = {}
        self.matches = {}
        self.running = True
    
    def display_menu(self) -> None:
        """Display the main menu."""
        print("\n" + "="*50)
        print("      CRICKET SIMULATION GAME")
        print("="*50)
        print("\n1. Manage Players")
        print("2. Manage Teams")
        print("3. Simulate Match")
        print("4. View Statistics")
        print("5. Exit")
        print("\n" + "="*50)
    
    def manage_players_menu(self) -> None:
        """Display player management menu."""
        while True:
            print("\n--- Player Management ---")
            print("1. Create Player")
            print("2. View Players")
            print("3. Back to Main Menu")
            
            choice = input("\nEnter your choice: ").strip()
            
            if choice == "1":
                self.create_player()
            elif choice == "2":
                self.view_players()
            elif choice == "3":
                break
            else:
                print("Invalid choice. Please try again.")
    
    def create_player(self) -> None:
        """Create a new player."""
        print("\n--- Create New Player ---")
        player_id = input("Player ID: ").strip()
        
        if player_id in self.players:
            print(f"Player with ID '{player_id}' already exists!")
            return
        
        name = input("Player Name: ").strip()
        role = input("Role (batsman/bowler/all-rounder/wicket-keeper): ").strip()
        
        if role not in ["batsman", "bowler", "all-rounder", "wicket-keeper"]:
            print("Invalid role. Defaulting to 'batsman'.")
            role = "batsman"
        
        player = Player(player_id, name, role=role)
        self.players[player_id] = player
        print(f"\n✓ Player '{name}' created successfully!")
    
    def view_players(self) -> None:
        """Display all players."""
        if not self.players:
            print("\nNo players found. Create some players first!")
            return
        
        print("\n--- All Players ---")
        for player in self.players.values():
            print(f"\n{player.get_summary()}")
    
    def manage_teams_menu(self) -> None:
        """Display team management menu."""
        while True:
            print("\n--- Team Management ---")
            print("1. Create Team")
            print("2. Add Player to Team")
            print("3. View Teams")
            print("4. Back to Main Menu")
            
            choice = input("\nEnter your choice: ").strip()
            
            if choice == "1":
                self.create_team()
            elif choice == "2":
                self.add_player_to_team()
            elif choice == "3":
                self.view_teams()
            elif choice == "4":
                break
            else:
                print("Invalid choice. Please try again.")
    
    def create_team(self) -> None:
        """Create a new team."""
        print("\n--- Create New Team ---")
        team_id = input("Team ID: ").strip()
        
        if team_id in self.teams:
            print(f"Team with ID '{team_id}' already exists!")
            return
        
        name = input("Team Name: ").strip()
        
        team = Team(team_id, name)
        self.teams[team_id] = team
        print(f"\n✓ Team '{name}' created successfully!")
    
    def add_player_to_team(self) -> None:
        """Add a player to a team."""
        if not self.teams:
            print("\nNo teams found. Create a team first!")
            return
        
        if not self.players:
            print("\nNo players found. Create some players first!")
            return
        
        print("\n--- Add Player to Team ---")
        team_id = input("Team ID: ").strip()
        
        if team_id not in self.teams:
            print(f"Team with ID '{team_id}' not found!")
            return
        
        player_id = input("Player ID: ").strip()
        
        if player_id not in self.players:
            print(f"Player with ID '{player_id}' not found!")
            return
        
        team = self.teams[team_id]
        player = self.players[player_id]
        
        if team.add_player(player):
            print(f"\n✓ Player '{player.name}' added to team '{team.name}'!")
        else:
            print(f"\n✗ Team '{team.name}' roster is full!")
    
    def view_teams(self) -> None:
        """Display all teams."""
        if not self.teams:
            print("\nNo teams found. Create some teams first!")
            return
        
        print("\n--- All Teams ---")
        for team in self.teams.values():
            print(team.get_summary())
    
    def simulate_match_menu(self) -> None:
        """Match simulation menu (placeholder)."""
        print("\n--- Simulate Match ---")
        print("Match simulation feature coming soon!")
        print("This will allow you to simulate matches between teams.")
        input("\nPress Enter to continue...")
    
    def view_statistics_menu(self) -> None:
        """Statistics viewing menu (placeholder)."""
        print("\n--- View Statistics ---")
        print("Statistics feature coming soon!")
        print("This will show detailed player and team statistics.")
        input("\nPress Enter to continue...")
    
    def run(self) -> None:
        """Run the main application loop."""
        print("\nWelcome to Cricket Simulation Game!")
        
        while self.running:
            self.display_menu()
            choice = input("\nEnter your choice: ").strip()
            
            if choice == "1":
                self.manage_players_menu()
            elif choice == "2":
                self.manage_teams_menu()
            elif choice == "3":
                self.simulate_match_menu()
            elif choice == "4":
                self.view_statistics_menu()
            elif choice == "5":
                print("\nThank you for playing Cricket Simulation Game!")
                print("Goodbye!\n")
                self.running = False
            else:
                print("\nInvalid choice. Please enter a number between 1 and 5.")


def main() -> int:
    """
    Main entry point for the application.
    
    Returns:
        Exit code (0 for success, 1 for error)
    """
    try:
        cli = CricketSimulationCLI()
        cli.run()
        return 0
    except KeyboardInterrupt:
        print("\n\nApplication interrupted by user. Exiting...")
        return 0
    except Exception as e:
        print(f"\nAn error occurred: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
