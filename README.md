# Roguelike Game

A classic roguelike game implemented in Python using the TCOD library, inspired by the original Rogue (1980s).

[日本語版はこちら](README-jp.md)

## Features

- Classic ASCII-based graphics using TCOD library
- Procedurally generated dungeons
- Turn-based combat system
- Various items and equipment
- Monster AI with FOV and tracking
- Classic roguelike mechanics (hunger, inventory management, etc.)

## Requirements

- Python 3.9+
- TCOD library
- Other dependencies listed in `requirements.txt`

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/roguelike.git
cd roguelike
```

2. Create a virtual environment (recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## How to Play

Run the game:
```bash
python src/main.py
```

### Controls

- Arrow keys or hjkl: Move
- g: Pick up items
- i: Open inventory
- d: Drop item
- ESC: Quit game
- ?: Help

## Development

For development, install additional dependencies:
```bash
pip install -r requirements-dev.txt
```

Run tests:
```bash
pytest
```

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Original Rogue game creators
- TCOD library developers
- Python community
- Cursor - AI pair programming assistant 