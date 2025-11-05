#!/usr/bin/env python3
"""
Play Match - Interactive Cricket Match Simulation

A simple script to load sample teams, let users choose teams and format,
and simulate a cricket match with detailed scorecard.
"""

import sys
from src.data.data_loader import get_default_teams, get_team_by_name, list_available_teams
from src.models.match import Match, MatchFormat
from src.simulation.engine import SimulationEngine


def print_banner():
    """Print a welcome banner."""
    print("\n" + "="*70)
    print(" "*20 + "CRICKET MATCH SIMULATION")
    print("="*70 + "\n")


def select_team(teams, team_number):
    """
    Let user select a team.
    
    Args:
        teams: List of available teams
        team_number: Which team is being selected (1 or 2)
    
    Returns:
        Selected Team object
    """
    print(f"\nSelect Team {team_number}:")
    team_names = list_available_teams(teams)
    
    for i, name in enumerate(team_names, 1):
        print(f"{i}. {name}")
    
    while True:
        try:
            choice = input(f"\nEnter your choice (1-{len(team_names)}): ").strip()
            choice_idx = int(choice) - 1
            
            if 0 <= choice_idx < len(team_names):
                team_name = team_names[choice_idx]
                return get_team_by_name(teams, team_name)
            else:
                print(f"Invalid choice. Please enter a number between 1 and {len(team_names)}.")
        except ValueError:
            print("Invalid input. Please enter a number.")


def select_format():
    """
    Let user select match format.
    
    Returns:
        MatchFormat enum value
    """
    print("\nSelect Match Format:")
    print("1. T20 (20 overs)")
    print("2. ODI (50 overs)")
    
    while True:
        try:
            choice = input("\nEnter your choice (1-2): ").strip()
            
            if choice == "1":
                return MatchFormat.T20
            elif choice == "2":
                return MatchFormat.ODI
            else:
                print("Invalid choice. Please enter 1 or 2.")
        except ValueError:
            print("Invalid input. Please enter a number.")


def display_team_summary(team):
    """
    Display a summary of the team.
    
    Args:
        team: Team object
    """
    print(f"\n{team.name} Playing XI:")
    print("-" * 50)
    
    batting_order = team.get_batting_order()
    for i, player in enumerate(batting_order, 1):
        avg = player.batting_stats.average
        sr = player.batting_stats.strike_rate
        print(f"{i:2d}. {player.name:<25} ({player.role:<15}) Avg: {avg:.1f}, SR: {sr:.1f}")
    
    print("\nKey Bowlers:")
    print("-" * 50)
    bowlers = team.get_bowlers()[:5]  # Top 5 bowlers
    for player in bowlers:
        avg = player.bowling_stats.average
        econ = player.bowling_stats.economy
        print(f"    {player.name:<25} Avg: {avg:.1f}, Econ: {econ:.1f}")


def main():
    """Main function to run the match simulation."""
    try:
        print_banner()
        
        # Load teams
        print("Loading teams...")
        teams = get_default_teams()
        print(f"Loaded {len(teams)} teams successfully!\n")
        
        # Select teams
        team1 = select_team(teams, 1)
        team2 = select_team(teams, 2)
        
        # Prevent selecting same team twice
        while team1.name == team2.name:
            print("\nYou cannot select the same team twice!")
            team2 = select_team(teams, 2)
        
        # Select format
        match_format = select_format()
        
        # Display team summaries
        print("\n" + "="*70)
        print("MATCH PREVIEW")
        print("="*70)
        display_team_summary(team1)
        display_team_summary(team2)
        
        # Confirm before starting
        print("\n" + "="*70)
        print(f"\nMatch: {team1.name} vs {team2.name}")
        print(f"Format: {match_format.value}")
        print("\n" + "="*70)
        
        input("\nPress Enter to start the match simulation...")
        
        # Create match
        match = Match(
            match_id="MATCH_001",
            team_a=team1,
            team_b=team2,
            format=match_format,
            venue="Simulation Stadium"
        )
        
        # Run simulation
        print("\nSimulating match...")
        print("(This may take a moment...)\n")
        
        engine = SimulationEngine(match, verbose=True)
        result = engine.simulate_match()
        
        # Display scorecard
        print("\n" + result.generate_scorecard())
        
        # Display summary
        print("\n" + "="*70)
        print("MATCH SUMMARY")
        print("="*70)
        print(f"\n{team1.name}: {result.team_a_score}/{result.team_a_wickets} ({result.team_a_overs} overs)")
        print(f"{team2.name}: {result.team_b_score}/{result.team_b_wickets} ({result.team_b_overs} overs)")
        print(f"\nResult: {result.result_text}")
        
        if result.player_of_match:
            print(f"\nPlayer of the Match: {result.player_of_match.name}")
        
        # Top performers
        print("\n" + "="*70)
        print("TOP PERFORMERS")
        print("="*70)
        
        # Top scorers
        all_batting = {**result.innings1.batting_scores, **result.innings2.batting_scores}
        if all_batting:
            top_scorers = sorted(all_batting.items(), key=lambda x: x[1], reverse=True)[:3]
            print("\nTop Scorers:")
            for i, (name, runs) in enumerate(top_scorers, 1):
                balls = result.innings1.batting_balls.get(name, 0) + result.innings2.batting_balls.get(name, 0)
                print(f"{i}. {name}: {runs} runs ({balls} balls)")
        
        # Best bowlers
        all_bowling = {**result.innings1.bowling_figures, **result.innings2.bowling_figures}
        if all_bowling:
            top_bowlers = sorted(all_bowling.items(), 
                               key=lambda x: (x[1].get('wickets', 0), -x[1].get('runs', 999)), 
                               reverse=True)[:3]
            print("\nBest Bowlers:")
            for i, (name, figures) in enumerate(top_bowlers, 1):
                wickets = figures.get('wickets', 0)
                runs = figures.get('runs', 0)
                overs = figures.get('overs', 0)
                print(f"{i}. {name}: {wickets} wickets for {runs} runs ({overs} overs)")
        
        print("\n" + "="*70)
        print("\nThank you for using Cricket Match Simulation!")
        print("="*70 + "\n")
        
        return 0
        
    except KeyboardInterrupt:
        print("\n\nSimulation interrupted by user. Exiting...")
        return 0
    except Exception as e:
        print(f"\nAn error occurred: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
