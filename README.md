# Rogue like

[Japanese version below](README-jp.md)

## Overview
This project is a Python implementation of the classic 1980s roguelike game "Rogue". It aims to faithfully recreate the original specifications and behavior while employing modern code design principles.

## Features
- Faithful recreation of original Rogue
- Procedural dungeon generation
- Turn-based combat system
- Traditional ASCII art display
- Score system with rankings

## Tech Stack
- Python 3.8+
- blessed (terminal handling)
- injector (dependency injection)
- dataclasses (data models)

## Installation

```bash
git clone https://github.com/yuru-sha/roguelike.git
cd roguelike
pip install -r requirements.txt
```

## Running

```bash
python src/main.py
```

## Project Structure

```
src/
├── core/ # Game engine and core logic
├── entities/ # Game entities
├── utils/ # Utility functions
└── constants/ # Game constants
```

## License
MIT License
