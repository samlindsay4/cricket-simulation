"""
Cricket match simulation engine.

This module contains the core simulation logic for simulating cricket matches
ball by ball with realistic probabilities.
"""

import random
from typing import Dict, Any, Optional, List, Tuple
from ..models.player import Player
from ..models.team import Team
from ..models.match import Match, MatchFormat, MatchStatus, InningsData


class BallResult:
    """Result of a single ball."""
    
    def __init__(self, runs: int, is_wicket: bool, is_extra: bool = False,
                 extra_type: str = "", batsman: Optional[Player] = None,
                 bowler: Optional[Player] = None):
        self.runs = runs
        self.is_wicket = is_wicket
        self.is_extra = is_extra
        self.extra_type = extra_type  # "wide", "no-ball", etc.
        self.batsman = batsman
        self.bowler = bowler
    
    def __repr__(self) -> str:
        if self.is_wicket:
            return f"WICKET! ({self.batsman.name if self.batsman else 'Unknown'})"
        elif self.is_extra:
            return f"{self.extra_type}: {self.runs} run(s)"
        else:
            return f"{self.runs} run(s)"


class SimulationEngine:
    """
    Core simulation engine for cricket matches.
    
    Simulates matches ball by ball with realistic probabilities based on
    player statistics.
    """
    
    def __init__(self, match: Match, verbose: bool = False):
        """
        Initialize the simulation engine.
        
        Args:
            match: The match to simulate
            verbose: If True, print ball-by-ball commentary
        """
        self.match = match
        self.verbose = verbose
        self.current_innings: Optional[InningsData] = None
        self.batting_team: Optional[Team] = None
        self.bowling_team: Optional[Team] = None
        self.batsmen_index = 0  # Track which batsman to send next
        self.bowler_index = 0  # Track bowler rotation
        self.bowler_overs: Dict[str, int] = {}  # Track overs bowled by each bowler
    
    def simulate_ball(self, batsman: Player, bowler: Player) -> BallResult:
        """
        Simulate a single ball delivery.
        
        Uses realistic probabilities based on batsman and bowler statistics.
        
        Args:
            batsman: The batsman facing
            bowler: The bowler bowling
        
        Returns:
            BallResult object with outcome
        """
        # Small chance of extras (5%)
        if random.random() < 0.05:
            extra_type = "wide" if random.random() < 0.7 else "no-ball"
            runs = 1 if extra_type == "wide" else (1 + random.randint(0, 1))
            return BallResult(runs, False, True, extra_type, batsman, bowler)
        
        # Check for wicket
        dismissal_prob = batsman.calculate_dismissal_probability(bowler)
        if random.random() < dismissal_prob:
            return BallResult(0, True, False, "", batsman, bowler)
        
        # Calculate runs scored
        scoring_probs = batsman.calculate_scoring_probabilities(bowler)
        
        # Generate random number and determine outcome
        rand = random.random()
        cumulative = 0.0
        
        for runs, prob in sorted(scoring_probs.items()):
            cumulative += prob
            if rand < cumulative:
                return BallResult(runs, False, False, "", batsman, bowler)
        
        # Fallback to dot ball
        return BallResult(0, False, False, "", batsman, bowler)
    
    def simulate_innings(self, batting_team: Team, bowling_team: Team,
                        target: Optional[int] = None) -> InningsData:
        """
        Simulate a complete innings.
        
        Args:
            batting_team: Team batting
            bowling_team: Team bowling
            target: Target score to chase (optional)
        
        Returns:
            InningsData with complete innings information
        """
        innings = InningsData()
        self.current_innings = innings
        self.batting_team = batting_team
        self.bowling_team = bowling_team
        
        # Get batting order and bowlers
        batting_order = batting_team.get_batting_order()
        bowlers = bowling_team.get_bowlers()
        
        if len(batting_order) < 2:
            raise ValueError(f"Team {batting_team.name} needs at least 2 players")
        if len(bowlers) < 1:
            raise ValueError(f"Team {bowling_team.name} needs at least 1 bowler")
        
        # Initialize batsmen
        striker = batting_order[0]
        non_striker = batting_order[1]
        self.batsmen_index = 2
        
        innings.batting_scores[striker.name] = 0
        innings.batting_balls[striker.name] = 0
        innings.batting_scores[non_striker.name] = 0
        innings.batting_balls[non_striker.name] = 0
        
        # Initialize first bowler
        self.bowler_index = 0
        current_bowler = bowlers[self.bowler_index % len(bowlers)]
        self.bowler_overs = {b.name: 0 for b in bowlers}
        
        max_overs = self.match.get_max_overs()
        
        if self.verbose:
            print(f"\n{'='*60}")
            print(f"{batting_team.name} Innings")
            print(f"{'='*60}\n")
        
        # Simulate ball by ball
        while innings.wickets < 10 and innings.overs < max_overs:
            # Check if target achieved
            if target and innings.score >= target:
                if self.verbose:
                    print(f"\nTarget achieved! {batting_team.name} wins!")
                break
            
            # Simulate the ball
            result = self.simulate_ball(striker, current_bowler)
            
            # Update innings data
            if result.is_extra:
                innings.extras += result.runs
                innings.score += result.runs
                
                # Initialize bowler if not in figures yet
                if current_bowler.name not in innings.bowling_figures:
                    innings.bowling_figures[current_bowler.name] = {
                        'overs': 0, 'runs': 0, 'wickets': 0
                    }
                innings.bowling_figures[current_bowler.name]['runs'] += result.runs
                
                if self.verbose:
                    print(f"{innings.overs}.{innings.balls}: {result} by {current_bowler.name}")
                
                # Wide/no-ball doesn't count as a legal delivery
                continue
            
            # Legal delivery
            innings.balls += 1
            innings.batting_balls[striker.name] += 1
            
            # Initialize bowler if not in figures yet
            if current_bowler.name not in innings.bowling_figures:
                innings.bowling_figures[current_bowler.name] = {
                    'overs': 0, 'runs': 0, 'wickets': 0
                }
            
            if result.is_wicket:
                innings.wickets += 1
                innings.bowling_figures[current_bowler.name]['wickets'] += 1
                innings.fall_of_wickets.append((innings.score, innings.wickets, striker.name))
                
                if self.verbose:
                    print(f"{innings.overs}.{innings.balls}: WICKET! {striker.name} out! "
                          f"Score: {innings.score}/{innings.wickets}")
                
                # New batsman comes in
                if self.batsmen_index < len(batting_order):
                    striker = batting_order[self.batsmen_index]
                    self.batsmen_index += 1
                    innings.batting_scores[striker.name] = 0
                    innings.batting_balls[striker.name] = 0
                    
                    if self.verbose:
                        print(f"  {striker.name} comes to the crease")
                else:
                    # All out
                    break
            else:
                # Runs scored
                innings.score += result.runs
                innings.batting_scores[striker.name] += result.runs
                innings.bowling_figures[current_bowler.name]['runs'] += result.runs
                
                if self.verbose and (result.runs >= 4 or innings.balls == 6):
                    print(f"{innings.overs}.{innings.balls}: {result.runs} run(s) by {striker.name} "
                          f"off {current_bowler.name} - Score: {innings.score}/{innings.wickets}")
                
                # Swap batsmen on odd runs
                if result.runs % 2 == 1:
                    striker, non_striker = non_striker, striker
            
            # End of over
            if innings.balls == 6:
                innings.overs += 1
                innings.balls = 0
                self.bowler_overs[current_bowler.name] += 1
                innings.bowling_figures[current_bowler.name]['overs'] += 1
                
                # Swap batsmen at end of over
                striker, non_striker = non_striker, striker
                
                # Change bowler
                self.bowler_index += 1
                current_bowler = bowlers[self.bowler_index % len(bowlers)]
                
                if self.verbose:
                    print(f"\nEnd of over {innings.overs}. Score: {innings.score}/{innings.wickets}")
                    print(f"{current_bowler.name} to bowl next over\n")
        
        if self.verbose:
            print(f"\n{'='*60}")
            print(f"End of Innings: {innings.score}/{innings.wickets} "
                  f"({innings.overs}.{innings.balls} overs)")
            print(f"{'='*60}\n")
        
        return innings
    
    def simulate_match(self) -> Match:
        """
        Simulate a complete match.
        
        Simulates both innings, determines winner, and selects player of the match.
        
        Returns:
            The match object with complete results
        """
        self.match.status = MatchStatus.IN_PROGRESS
        
        # Conduct toss (random for now)
        toss_winner = random.choice([self.match.team_a, self.match.team_b])
        # In T20, teams usually bat first; in ODI it's more varied
        elected_to = "bat" if random.random() < 0.6 else "bowl"
        self.match.conduct_toss(toss_winner, elected_to)
        
        # Determine batting order
        if elected_to == "bat":
            first_batting = toss_winner
            first_bowling = self.match.team_b if toss_winner == self.match.team_a else self.match.team_a
        else:
            first_bowling = toss_winner
            first_batting = self.match.team_b if toss_winner == self.match.team_a else self.match.team_a
        
        if self.verbose:
            print(f"\n{'='*60}")
            print(f"MATCH: {self.match.team_a.name} vs {self.match.team_b.name}")
            print(f"Format: {self.match.format.value}")
            print(f"Venue: {self.match.venue}")
            print(f"{'='*60}")
            print(f"\nToss: {toss_winner.name} won and elected to {elected_to}")
            print(f"{first_batting.name} will bat first\n")
        
        # First innings
        self.match.innings1 = self.simulate_innings(first_batting, first_bowling)
        
        # Update match scores
        if first_batting == self.match.team_a:
            self.match.team_a_score = self.match.innings1.score
            self.match.team_a_wickets = self.match.innings1.wickets
            self.match.team_a_overs = self.match.innings1.get_overs_float()
        else:
            self.match.team_b_score = self.match.innings1.score
            self.match.team_b_wickets = self.match.innings1.wickets
            self.match.team_b_overs = self.match.innings1.get_overs_float()
        
        target = self.match.innings1.score + 1
        
        if self.verbose:
            print(f"\nTarget for {first_bowling.name}: {target} runs\n")
        
        # Second innings
        self.match.innings2 = self.simulate_innings(first_bowling, first_batting, target)
        
        # Update match scores
        if first_bowling == self.match.team_a:
            self.match.team_a_score = self.match.innings2.score
            self.match.team_a_wickets = self.match.innings2.wickets
            self.match.team_a_overs = self.match.innings2.get_overs_float()
        else:
            self.match.team_b_score = self.match.innings2.score
            self.match.team_b_wickets = self.match.innings2.wickets
            self.match.team_b_overs = self.match.innings2.get_overs_float()
        
        # Determine winner
        first_innings_score = self.match.innings1.score
        second_innings_score = self.match.innings2.score
        
        if second_innings_score > first_innings_score:
            self.match.winner = first_bowling
            runs_margin = second_innings_score - first_innings_score
            wickets_left = 10 - self.match.innings2.wickets
            self.match.result_text = f"{first_bowling.name} won by {wickets_left} wickets"
        elif second_innings_score < first_innings_score:
            self.match.winner = first_batting
            runs_margin = first_innings_score - second_innings_score
            self.match.result_text = f"{first_batting.name} won by {runs_margin} runs"
        else:
            self.match.winner = None
            self.match.result_text = "Match tied"
        
        # Select player of the match (simple: highest runs or most wickets)
        self.match.player_of_match = self._select_player_of_match()
        
        self.match.status = MatchStatus.COMPLETED
        
        if self.verbose:
            print(f"\n{'='*60}")
            print(f"MATCH RESULT")
            print(f"{'='*60}")
            print(f"{self.match.team_a.name}: {self.match.team_a_score}/{self.match.team_a_wickets}")
            print(f"{self.match.team_b.name}: {self.match.team_b_score}/{self.match.team_b_wickets}")
            print(f"\n{self.match.result_text}")
            if self.match.player_of_match:
                print(f"Player of the Match: {self.match.player_of_match.name}")
            print(f"{'='*60}\n")
        
        return self.match
    
    def _select_player_of_match(self) -> Optional[Player]:
        """
        Select player of the match based on performance.
        
        Simple algorithm: highest runs or most wickets.
        
        Returns:
            Player of the match
        """
        all_batting = {**self.match.innings1.batting_scores, **self.match.innings2.batting_scores}
        all_bowling = {**self.match.innings1.bowling_figures, **self.match.innings2.bowling_figures}
        
        # Find highest scorer
        if all_batting:
            top_scorer_name = max(all_batting, key=all_batting.get)
            top_score = all_batting[top_scorer_name]
        else:
            top_scorer_name = None
            top_score = 0
        
        # Find best bowler
        if all_bowling:
            top_bowler_name = max(all_bowling, key=lambda x: all_bowling[x].get('wickets', 0))
            top_wickets = all_bowling[top_bowler_name].get('wickets', 0)
        else:
            top_bowler_name = None
            top_wickets = 0
        
        # Simple heuristic: 3+ wickets or 50+ runs
        if top_wickets >= 3:
            # Find the player object
            for team in [self.match.team_a, self.match.team_b]:
                for player in team.players:
                    if player.name == top_bowler_name:
                        return player
        
        if top_score >= 40:
            # Find the player object
            for team in [self.match.team_a, self.match.team_b]:
                for player in team.players:
                    if player.name == top_scorer_name:
                        return player
        
        # Otherwise, highest scorer
        if top_scorer_name:
            for team in [self.match.team_a, self.match.team_b]:
                for player in team.players:
                    if player.name == top_scorer_name:
                        return player
        
        return None
