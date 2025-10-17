##  Architecture & Design

### Functional Programming Principles

This implementation strictly follows functional programming paradigms:

#### 1. **Immutability**
```python
@dataclass(frozen=True)
class GameState:
    """Immutable game state"""
    board: Tuple[Tuple[int, ...], ...]
    score: int
    size: int
    game_over: bool
    won: bool
```
- All game state is immutable
- Every operation returns a new state
- No in-place modifications

#### 2. **Pure Functions**
All core game logic uses pure functions:
- `create_empty_board()`: Creates initial board
- `move_left()`, `move_right()`, `move_up()`, `move_down()`: Movement logic
- `can_move()`: Checks if moves are available
- `has_won()`: Checks win condition

Example:
```python
def move_left(board: Tuple[Tuple[int, ...], ...]) -> Tuple[Tuple[Tuple[int, ...], ...], int]:
    """Pure function - no side effects, returns new board and score"""
    new_board = []
    total_score = 0

    for row in board:
        new_row, score = process_line(list(row))
        new_board.append(tuple(new_row))
        total_score += score

    return tuple(new_board), total_score
```

#### 3. **Separation of Concerns**
- **Core Logic** (functional): Pure game mechanics
- **GUI Layer**: Handles display and user interaction
- **State Management**: Immutable state transitions

### Code Structure

```
game_2048.py
├── Functional Core (Immutable Operations)
│   ├── GameState (immutable dataclass)
│   ├── Board operations (pure functions)
│   ├── Movement logic (pure functions)
│   └── Game state transitions (pure functions)
│
└── GUI Implementation
    ├── Game2048GUI (class)
    ├── Display management
    ├── Animation system
    └── Event handling
```

### Key Algorithms

#### 1. **Tile Movement Algorithm**
```python
def process_line(line: List[int]) -> Tuple[List[int], int]:
    # 1. Compress: Move all non-zero tiles to one side
    # 2. Merge: Combine adjacent equal tiles
    # 3. Compress: Move again to fill gaps
```

#### 2. **Move Transformation**
- **Left**: Process each row left-to-right
- **Right**: Reverse → Move Left → Reverse
- **Up**: Transpose → Move Left → Transpose
- **Down**: Transpose → Move Right → Transpose

#### 3. **State Transition**
```python
def apply_move(state: GameState, direction: Direction) -> GameState:
    # 1. Apply movement transformation
    # 2. Check if board changed
    # 3. Add new random tile
    # 4. Check win/lose conditions
    # 5. Return new immutable state
```

#### 1. Board Movement
```python
def process_line(line: List[int]) -> Tuple[List[int], int]:
    # Example: [2, 2, 4, 0]
    # After compress: [2, 2, 4, 0]
    # After merge: [4, 0, 4, 0]
    # After compress: [4, 4, 0, 0]
    # Score: 4 (from merging 2+2)
```

#### 2. State Transitions
```python
# Immutable state flow:
state1 = GameState(board1, score=0, ...)
state2 = apply_move(state1, Direction.LEFT)
# state1 unchanged, state2 is new state
```

#### 3. Win/Lose Detection
```python
# Winning: 2048 tile exists
# Losing: No empty cells AND no adjacent equal tiles
```
