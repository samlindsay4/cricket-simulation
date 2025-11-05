# Cricket Simulation Game

A comprehensive cricket simulation game built with Python that allows you to create teams, manage players, and simulate realistic cricket matches with detailed statistics.

## Overview

The Cricket Simulation Game is a text-based application that simulates cricket matches using statistical models and realistic game mechanics. Whether you're a cricket enthusiast, a developer learning game simulation, or someone interested in sports analytics, this project provides a solid foundation for cricket match simulation.

## Features

### Current Features
- **Player Management**: Create and manage cricket players with detailed statistics
  - Batting stats (runs, average, strike rate, centuries, etc.)
  - Bowling stats (wickets, economy, average, strike rate, etc.)
  - Fielding stats (catches, stumpings, run-outs)
- **Team Management**: Build and organize cricket teams
  - Add/remove players from teams
  - Set team captains
  - Manage squad rosters (up to 15 players)
- **Match Context**: Set up matches between teams
  - Support for multiple formats (T20, ODI, Test)
  - Toss simulation
  - Match status tracking

### Planned Features (Development Roadmap)
1. ✅ Initial project setup and architecture (Issue #1)
2. ⏳ Core simulation engine for ball-by-ball match simulation (Issue #2)
3. ⏳ Player statistics and rating system (Issue #3)
4. ⏳ Real player data integration (Issue #4)
5. ⏳ Team selection and strategy system (Issue #5)
6. ⏳ Match types and formats (T20, ODI, Test) (Issue #6)
7. ⏳ Tournament mode with fixtures and standings (Issue #7)
8. ⏳ Advanced statistics and analytics dashboard (Issue #8)
9. ⏳ Save/load game functionality (Issue #9)
10. ⏳ Enhanced user interface with visualization (Issue #10)

## Installation

### Prerequisites
- Python 3.8 or higher
- pip (Python package installer)

### Setup Instructions

1. **Clone the repository**
   ```bash
   git clone https://github.com/samlindsay4/cricket-simulation.git
   cd cricket-simulation
   ```

2. **Create a virtual environment** (recommended)
   ```bash
   # On Windows
   python -m venv venv
   venv\Scripts\activate

   # On macOS/Linux
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application**
   ```bash
   python main.py
   ```

## Quick Start Guide

1. **Launch the application**
   ```bash
   python main.py
   ```

2. **Create players**
   - Select option 1 (Manage Players)
   - Create new players with different roles (batsman, bowler, all-rounder, wicket-keeper)

3. **Build teams**
   - Select option 2 (Manage Teams)
   - Create teams and add players to them

4. **Simulate matches** (Coming Soon)
   - Select option 3 (Simulate Match)
   - Choose teams and watch the simulation unfold

## Project Structure

```
cricket-simulation/
│
├── src/                      # Main source code directory
│   ├── models/              # Data models
│   │   ├── player.py       # Player class with stats
│   │   ├── team.py         # Team class with roster management
│   │   └── match.py        # Match class for game context
│   │
│   ├── simulation/          # Core game engine (coming soon)
│   ├── data/               # Data loading and processing
│   ├── stats/              # Statistics calculation
│   └── ui/                 # User interface components
│
├── data/                    # Data storage
│   ├── players/            # Player statistics
│   └── teams/              # Team rosters
│
├── tests/                   # Unit and integration tests
├── docs/                    # Documentation
│
├── main.py                  # Application entry point
├── requirements.txt         # Python dependencies
├── .gitignore              # Git ignore rules
├── LICENSE                  # MIT License
└── README.md               # This file
```

## Development

### Running Tests
```bash
pytest tests/
```

### Code Style
This project follows PEP 8 style guidelines. All code includes:
- Type hints for function parameters and return values
- Comprehensive docstrings for classes and methods
- Clear, readable variable and function names

### Contributing

We welcome contributions! Here's how you can help:

1. **Fork the repository**
2. **Create a feature branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```
3. **Make your changes**
   - Write clean, documented code
   - Add tests for new features
   - Update documentation as needed
4. **Commit your changes**
   ```bash
   git commit -m "Add: brief description of your changes"
   ```
5. **Push to your fork**
   ```bash
   git push origin feature/your-feature-name
   ```
6. **Open a Pull Request**

### Development Roadmap

Check out our [Issues](https://github.com/samlindsay4/cricket-simulation/issues) page for the complete development roadmap. We have 10 major milestones planned:

- **Phase 1**: Foundation (Issues #1-2) - Project setup and core simulation
- **Phase 2**: Data & Players (Issues #3-4) - Player stats and real data
- **Phase 3**: Strategy & Formats (Issues #5-6) - Team selection and match types
- **Phase 4**: Advanced Features (Issues #7-10) - Tournaments, analytics, and UI

## Dependencies

- **pandas** (>=2.0.0) - Data manipulation and analysis
- **numpy** (>=1.24.0) - Numerical computations
- **pytest** (>=7.4.0) - Testing framework
- **python-dateutil** (>=2.8.2) - Date/time utilities

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Inspired by the love of cricket and sports simulation games
- Built with Python and modern software development practices
- Thanks to the open-source community for the excellent libraries

## Contact

- **Project Repository**: [github.com/samlindsay4/cricket-simulation](https://github.com/samlindsay4/cricket-simulation)
- **Issue Tracker**: [github.com/samlindsay4/cricket-simulation/issues](https://github.com/samlindsay4/cricket-simulation/issues)

---

**Happy Simulating! 🏏**