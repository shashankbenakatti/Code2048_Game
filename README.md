# 2048 Game - Complete Implementation

A fully functional implementation of the popular 2048 game with a beautiful GUI, smooth animations, and configurable board size. Built following functional programming principles with immutability at its core.

## Features

- **Classic 2048 Gameplay**: Merge tiles to reach 2048!
- **Beautiful GUI**: Clean, modern interface with smooth animations
- **Configurable Board Size**: Play on any board from 4x4 to 10x10
- **Functional Programming**: Immutable data structures and pure functions
- **Score Tracking**: Keep track of your score as you play
- **Keyboard Controls**: Use arrow keys or WASD
- **Responsive Design**: Automatically adjusts to different board sizes
- **Win/Lose Detection**: Automatic game state management

## Requirements

- Python 3.7 or higher
- tkinter (usually comes with Python)

##  Installation

### Method 1: Direct Python Execution

1. **Clone the repository:**
```bash
git clone https://github.com/yourusername/2048-game.git
cd 2048-game
```

2. **Run the game:**
```bash
python game_2048.py
```

### Method 2: Create Executable (Windows)

1. **Install PyInstaller:**
```bash
pip install pyinstaller
```

2. **Create executable:**
```bash
pyinstaller --onefile --windowed --name 2048Game game_2048.py
```

3. **Find your executable:**
- The `.exe` file will be in the `dist` folder
- Double-click to run!

### Method 3: Create Executable (macOS/Linux)

1. **Install PyInstaller:**
```bash
pip install pyinstaller
```

2. **Create executable:**
```bash
pyinstaller --onefile --windowed --name 2048Game game_2048.py
```

3. **Run the application:**
```bash
./dist/2048Game
```

## How to Play

### Objective
Combine tiles with the same number to reach the **2048** tile!

### Controls
- **Arrow Keys**: ↑ ↓ ← → to move tiles
- **WASD Keys**: Alternative control scheme
  - W: Move up
  - S: Move down
  - A: Move left
  - D: Move right

### Game Rules

1. **Starting**: The game begins with two random tiles (2 or 4) on the board
2. **Moving**: Use arrow keys to slide all tiles in that direction
3. **Merging**: When two tiles with the same number touch, they merge into one
4. **Scoring**: Your score increases by the value of each merged tile
5. **New Tiles**: After each move, a new tile (2 or 4) appears randomly
6. **Winning**: Reach the 2048 tile (but you can continue playing!)
7. **Losing**: The game ends when no more moves are possible

### Tips
- Plan ahead! Try to keep your highest tile in a corner
- Build up tiles in one direction
- Don't spread high-value tiles across the board
- Keep the board as empty as possible

## Customization

### Board Size
1. Enter a number in the "Board Size" field (minimum 4, maximum 10)
2. Click "Apply" to create a new game with the selected size
3. The interface automatically adjusts to accommodate different sizes

### Color Scheme
The game uses a carefully designed color palette:
- Empty cells: Light beige (#CDC1B4)
- Low numbers (2, 4): Soft cream tones
- Medium numbers (8-64): Orange gradient
- High numbers (128-512): Yellow gradient
- 2048+: Dark colors for contrast
