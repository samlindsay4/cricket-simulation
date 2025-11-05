"""
Test suite for cricket simulation engine.

Tests player creation, team creation, and match simulation.
"""

import pytest
from src.models.player import Player
from src.models.team import Team
from src.models.match import Match, MatchFormat
from src.simulation.engine import SimulationEngine, BallResult
from src.data.data_loader import get_default_teams, load_teams_from_json, get_team_by_name


class TestPlayerCreation:
    """Test player creation and methods."""
    
    def test_create_batsman(self):
        """Test creating a batsman with stats."""
        player = Player(
            player_id="TEST_1",
            name="Test Batsman",
            role="batsman",
            batting_average=45.0,
            strike_rate=130.0
        )
        
        assert player.name == "Test Batsman"
        assert player.role == "batsman"
        assert player.batting_stats.average == 45.0
        assert player.batting_stats.strike_rate == 130.0
    
    def test_create_bowler(self):
        """Test creating a bowler with stats."""
        player = Player(
            player_id="TEST_2",
            name="Test Bowler",
            role="bowler",
            bowling_average=25.0,
            economy_rate=6.0
        )
        
        assert player.name == "Test Bowler"
        assert player.role == "bowler"
        assert player.bowling_stats.average == 25.0
        assert player.bowling_stats.economy == 6.0
    
    def test_dismissal_probability(self):
        """Test dismissal probability calculation."""
        batsman = Player(
            player_id="BAT_1",
            name="Good Batsman",
            role="batsman",
            batting_average=50.0
        )
        
        bowler = Player(
            player_id="BOWL_1",
            name="Good Bowler",
            role="bowler",
            bowling_average=25.0
        )
        
        prob = batsman.calculate_dismissal_probability(bowler)
        
        # Probability should be between 0.5% and 8%
        assert 0.005 <= prob <= 0.08
    
    def test_scoring_probabilities(self):
        """Test scoring probability calculation."""
        batsman = Player(
            player_id="BAT_1",
            name="Aggressive Batsman",
            role="batsman",
            batting_average=45.0,
            strike_rate=140.0
        )
        
        probs = batsman.calculate_scoring_probabilities()
        
        # Check all run outcomes are present
        assert 0 in probs
        assert 1 in probs
        assert 4 in probs
        assert 6 in probs
        
        # Probabilities should sum to approximately 1.0
        total = sum(probs.values())
        assert 0.99 <= total <= 1.01


class TestTeamCreation:
    """Test team creation and methods."""
    
    def test_create_team(self):
        """Test creating a team."""
        team = Team(team_id="TEST", name="Test Team")
        
        assert team.name == "Test Team"
        assert len(team.players) == 0
    
    def test_add_players(self):
        """Test adding players to a team."""
        team = Team(team_id="TEST", name="Test Team")
        
        player1 = Player("P1", "Player 1", role="batsman")
        player2 = Player("P2", "Player 2", role="bowler")
        
        assert team.add_player(player1) is True
        assert team.add_player(player2) is True
        assert len(team.players) == 2
    
    def test_team_max_players(self):
        """Test team cannot exceed 11 players."""
        team = Team(team_id="TEST", name="Test Team")
        
        # Add 11 players
        for i in range(11):
            player = Player(f"P{i}", f"Player {i}", role="batsman")
            assert team.add_player(player) is True
        
        # 12th player should fail
        extra_player = Player("P12", "Player 12", role="batsman")
        assert team.add_player(extra_player) is False
    
    def test_batting_order(self):
        """Test getting batting order."""
        team = Team(team_id="TEST", name="Test Team")
        
        # Add players with different roles
        team.add_player(Player("P1", "Batsman 1", role="batsman", batting_average=45.0))
        team.add_player(Player("P2", "Batsman 2", role="batsman", batting_average=40.0))
        team.add_player(Player("P3", "WK", role="wicket-keeper", batting_average=38.0))
        team.add_player(Player("P4", "All-rounder", role="all-rounder", batting_average=35.0))
        team.add_player(Player("P5", "Bowler 1", role="bowler", batting_average=10.0))
        team.add_player(Player("P6", "Bowler 2", role="bowler", batting_average=8.0))
        
        order = team.get_batting_order()
        
        assert len(order) == 6
        # Batsmen should come first
        assert order[0].role == "batsman"
        # Bowlers should be last
        assert order[-1].role == "bowler"
    
    def test_get_bowlers(self):
        """Test getting bowlers."""
        team = Team(team_id="TEST", name="Test Team")
        
        team.add_player(Player("P1", "Batsman", role="batsman"))
        team.add_player(Player("P2", "Bowler 1", role="bowler", bowling_average=25.0))
        team.add_player(Player("P3", "All-rounder", role="all-rounder", bowling_average=28.0))
        team.add_player(Player("P4", "Bowler 2", role="bowler", bowling_average=27.0))
        
        bowlers = team.get_bowlers()
        
        # Should have 3 bowlers (2 bowlers + 1 all-rounder)
        assert len(bowlers) == 3
        assert all(p.role in ["bowler", "all-rounder"] for p in bowlers)


class TestMatchCreation:
    """Test match creation."""
    
    def test_create_match(self):
        """Test creating a match."""
        team1 = Team("T1", "Team 1")
        team2 = Team("T2", "Team 2")
        
        match = Match(
            match_id="M1",
            team_a=team1,
            team_b=team2,
            format=MatchFormat.T20
        )
        
        assert match.team_a == team1
        assert match.team_b == team2
        assert match.format == MatchFormat.T20
    
    def test_match_max_overs(self):
        """Test getting max overs for different formats."""
        team1 = Team("T1", "Team 1")
        team2 = Team("T2", "Team 2")
        
        t20_match = Match("M1", team1, team2, format=MatchFormat.T20)
        assert t20_match.get_max_overs() == 20
        
        odi_match = Match("M2", team1, team2, format=MatchFormat.ODI)
        assert odi_match.get_max_overs() == 50


class TestSimulation:
    """Test simulation engine."""
    
    def create_test_team(self, team_id, name):
        """Helper to create a test team with 11 players."""
        team = Team(team_id, name)
        
        # Add 5 batsmen
        for i in range(5):
            team.add_player(Player(
                f"{team_id}_BAT{i}",
                f"{name} Batsman {i+1}",
                role="batsman",
                batting_average=40.0 + i*2,
                strike_rate=120.0 + i*5
            ))
        
        # Add 2 all-rounders
        for i in range(2):
            team.add_player(Player(
                f"{team_id}_AR{i}",
                f"{name} All-rounder {i+1}",
                role="all-rounder",
                batting_average=35.0,
                strike_rate=125.0,
                bowling_average=28.0,
                economy_rate=7.0
            ))
        
        # Add 1 wicket-keeper
        team.add_player(Player(
            f"{team_id}_WK",
            f"{name} Keeper",
            role="wicket-keeper",
            batting_average=38.0,
            strike_rate=115.0
        ))
        
        # Add 3 bowlers
        for i in range(3):
            team.add_player(Player(
                f"{team_id}_BOWL{i}",
                f"{name} Bowler {i+1}",
                role="bowler",
                batting_average=10.0,
                strike_rate=70.0,
                bowling_average=25.0 + i,
                economy_rate=6.0 + i*0.5
            ))
        
        return team
    
    def test_single_ball_simulation(self):
        """Test simulating a single ball."""
        team1 = self.create_test_team("T1", "Team 1")
        team2 = self.create_test_team("T2", "Team 2")
        
        match = Match("M1", team1, team2, format=MatchFormat.T20)
        engine = SimulationEngine(match, verbose=False)
        
        batsman = team1.players[0]
        bowler = team2.get_bowlers()[0]
        
        result = engine.simulate_ball(batsman, bowler)
        
        assert isinstance(result, BallResult)
        # Runs should be 0-6 or extra
        if not result.is_extra:
            assert result.runs in [0, 1, 2, 3, 4, 6]
    
    def test_full_innings_simulation(self):
        """Test simulating a full innings."""
        team1 = self.create_test_team("T1", "Team 1")
        team2 = self.create_test_team("T2", "Team 2")
        
        match = Match("M1", team1, team2, format=MatchFormat.T20)
        engine = SimulationEngine(match, verbose=False)
        
        innings = engine.simulate_innings(team1, team2)
        
        # Innings should complete (either all out or max overs)
        assert innings.wickets <= 10
        assert innings.overs <= 20
        
        # Score should be reasonable for T20
        assert 50 <= innings.score <= 250
    
    def test_full_match_simulation(self):
        """Test simulating a full match."""
        team1 = self.create_test_team("T1", "Team 1")
        team2 = self.create_test_team("T2", "Team 2")
        
        match = Match("M1", team1, team2, format=MatchFormat.T20)
        engine = SimulationEngine(match, verbose=False)
        
        result = engine.simulate_match()
        
        # Match should be completed
        assert result.status.value == "Completed"
        
        # Both teams should have scores
        assert result.team_a_score > 0
        assert result.team_b_score > 0
        
        # There should be a winner (or tie)
        assert result.winner in [team1, team2, None]
        
        # Scores should be realistic for T20
        assert 50 <= result.team_a_score <= 250
        assert 50 <= result.team_b_score <= 250
    
    def test_odi_match_simulation(self):
        """Test simulating an ODI match."""
        team1 = self.create_test_team("T1", "Team 1")
        team2 = self.create_test_team("T2", "Team 2")
        
        match = Match("M1", team1, team2, format=MatchFormat.ODI)
        engine = SimulationEngine(match, verbose=False)
        
        result = engine.simulate_match()
        
        # Match should be completed
        assert result.status.value == "Completed"
        
        # Scores should be realistic for ODI (higher than T20)
        # ODI scores can range from 150 to 500+
        assert 150 <= result.team_a_score <= 550
        assert 150 <= result.team_b_score <= 550


class TestDataLoader:
    """Test data loading functionality."""
    
    def test_load_default_teams(self):
        """Test loading default teams from JSON."""
        teams = get_default_teams()
        
        assert len(teams) >= 2
        assert all(isinstance(t, Team) for t in teams)
        
        # Each team should have 11 players
        for team in teams:
            assert len(team.players) == 11
    
    def test_get_team_by_name(self):
        """Test getting team by name."""
        teams = get_default_teams()
        
        # Should be able to find India
        india = get_team_by_name(teams, "India")
        assert india.name == "India"
        
        # Should raise error for non-existent team
        with pytest.raises(ValueError):
            get_team_by_name(teams, "NonExistent")
    
    def test_team_has_valid_players(self):
        """Test that loaded teams have valid players."""
        teams = get_default_teams()
        
        for team in teams:
            # Should have batsmen
            batsmen = [p for p in team.players if p.role == "batsman"]
            assert len(batsmen) > 0
            
            # Should have bowlers
            bowlers = team.get_bowlers()
            assert len(bowlers) >= 3
            
            # All players should have valid stats
            for player in team.players:
                assert player.batting_stats.average > 0
                assert player.batting_stats.strike_rate > 0


class TestScorecard:
    """Test scorecard generation."""
    
    def test_scorecard_generation(self):
        """Test generating a scorecard."""
        teams = get_default_teams()
        team1 = teams[0]
        team2 = teams[1]
        
        match = Match("M1", team1, team2, format=MatchFormat.T20)
        engine = SimulationEngine(match, verbose=False)
        
        result = engine.simulate_match()
        scorecard = result.generate_scorecard()
        
        # Scorecard should contain team names
        assert team1.name in scorecard
        assert team2.name in scorecard
        
        # Should contain scores
        assert str(result.team_a_score) in scorecard
        assert str(result.team_b_score) in scorecard
