"""
2048 Game Implementation
A fully functional 2048 game with GUI, following functional programming principles.
Author: Generated for SDE Assignment
Date: Oct 16 2025
"""

import tkinter as tk
from tkinter import messagebox, ttk
import random
import copy
from typing import List, Tuple, Optional, Dict
from dataclasses import dataclass
from enum import Enum

# ============================================================================
# FUNCTIONAL PROGRAMMING CORE - IMMUTABLE OPERATIONS
# ============================================================================

class Direction(Enum):
    """Enumeration for movement directions"""
    UP = "up"
    DOWN = "down"
    LEFT = "left"
    RIGHT = "right"

@dataclass(frozen=True)
class GameState:
    """Immutable game state following functional programming principles"""
    board: Tuple[Tuple[int, ...], ...]
    score: int
    size: int
    game_over: bool
    won: bool

    def to_dict(self) -> Dict:
        """Convert state to dictionary for easy access"""
        return {
            'board': [list(row) for row in self.board],
            'score': self.score,
            'size': self.size,
            'game_over': self.game_over,
            'won': self.won
        }

def create_empty_board(size: int) -> Tuple[Tuple[int, ...], ...]:
    """Create an empty board - pure function"""
    return tuple(tuple(0 for _ in range(size)) for _ in range(size))

def get_empty_cells(board: Tuple[Tuple[int, ...], ...]) -> List[Tuple[int, int]]:
    """Get list of empty cell positions - pure function"""
    empty = []
    for i in range(len(board)):
        for j in range(len(board[0])):
            if board[i][j] == 0:
                empty.append((i, j))
    return empty

def add_random_tile(board: Tuple[Tuple[int, ...], ...]) -> Tuple[Tuple[int, ...], ...]:
    """Add a random tile (2 or 4) to the board - returns new board"""
    empty_cells = get_empty_cells(board)
    if not empty_cells:
        return board

    row, col = random.choice(empty_cells)
    value = 2 if random.random() < 0.9 else 4

    # Create new board with immutability
    new_board = [list(row) for row in board]
    new_board[row][col] = value
    return tuple(tuple(row) for row in new_board)

def initialize_game(size: int) -> GameState:
    """Initialize a new game state - pure function"""
    board = create_empty_board(size)
    board = add_random_tile(board)
    board = add_random_tile(board)
    return GameState(board=board, score=0, size=size, game_over=False, won=False)

def compress_line(line: List[int]) -> Tuple[List[int], int]:
    """Compress a line by moving all non-zero elements to the left - pure function"""
    new_line = [num for num in line if num != 0]
    new_line.extend([0] * (len(line) - len(new_line)))
    return new_line, 0

def merge_line(line: List[int]) -> Tuple[List[int], int]:
    """Merge adjacent equal elements in a line - pure function"""
    score = 0
    new_line = line.copy()

    for i in range(len(new_line) - 1):
        if new_line[i] != 0 and new_line[i] == new_line[i + 1]:
            new_line[i] *= 2
            score += new_line[i]
            new_line[i + 1] = 0

    return new_line, score

def process_line(line: List[int]) -> Tuple[List[int], int]:
    """Process a line: compress, merge, compress again - pure function"""
    line, _ = compress_line(line)
    line, score = merge_line(line)
    line, _ = compress_line(line)
    return line, score

def move_left(board: Tuple[Tuple[int, ...], ...]) -> Tuple[Tuple[Tuple[int, ...], ...], int]:
    """Move all tiles left - pure function"""
    new_board = []
    total_score = 0

    for row in board:
        new_row, score = process_line(list(row))
        new_board.append(tuple(new_row))
        total_score += score

    return tuple(new_board), total_score

def transpose(board: Tuple[Tuple[int, ...], ...]) -> Tuple[Tuple[int, ...], ...]:
    """Transpose the board - pure function"""
    size = len(board)
    return tuple(tuple(board[j][i] for j in range(size)) for i in range(size))

def reverse_rows(board: Tuple[Tuple[int, ...], ...]) -> Tuple[Tuple[int, ...], ...]:
    """Reverse each row of the board - pure function"""
    return tuple(tuple(reversed(row)) for row in board)

def move_right(board: Tuple[Tuple[int, ...], ...]) -> Tuple[Tuple[Tuple[int, ...], ...], int]:
    """Move all tiles right - pure function"""
    board = reverse_rows(board)
    board, score = move_left(board)
    board = reverse_rows(board)
    return board, score

def move_up(board: Tuple[Tuple[int, ...], ...]) -> Tuple[Tuple[Tuple[int, ...], ...], int]:
    """Move all tiles up - pure function"""
    board = transpose(board)
    board, score = move_left(board)
    board = transpose(board)
    return board, score

def move_down(board: Tuple[Tuple[int, ...], ...]) -> Tuple[Tuple[Tuple[int, ...], ...], int]:
    """Move all tiles down - pure function"""
    board = transpose(board)
    board, score = move_right(board)
    board = transpose(board)
    return board, score

def boards_equal(board1: Tuple[Tuple[int, ...], ...],
                 board2: Tuple[Tuple[int, ...], ...]) -> bool:
    """Check if two boards are equal - pure function"""
    return board1 == board2

def can_move(board: Tuple[Tuple[int, ...], ...]) -> bool:
    """Check if any move is possible - pure function"""
    size = len(board)

    # Check for empty cells
    if get_empty_cells(board):
        return True

    # Check for possible merges horizontally
    for i in range(size):
        for j in range(size - 1):
            if board[i][j] == board[i][j + 1]:
                return True

    # Check for possible merges vertically
    for i in range(size - 1):
        for j in range(size):
            if board[i][j] == board[i + 1][j]:
                return True

    return False

def has_won(board: Tuple[Tuple[int, ...], ...]) -> bool:
    """Check if player has reached 2048 - pure function"""
    for row in board:
        if 2048 in row:
            return True
    return False

def apply_move(state: GameState, direction: Direction) -> GameState:
    """Apply a move to the game state - returns new immutable state"""
    move_functions = {
        Direction.LEFT: move_left,
        Direction.RIGHT: move_right,
        Direction.UP: move_up,
        Direction.DOWN: move_down
    }

    new_board, move_score = move_functions[direction](state.board)

    # If board didn't change, return same state
    if boards_equal(new_board, state.board):
        return state

    # Add random tile after successful move
    new_board = add_random_tile(new_board)
    new_score = state.score + move_score

    # Check win/lose conditions
    won = state.won or has_won(new_board)
    game_over = not can_move(new_board)

    return GameState(
        board=new_board,
        score=new_score,
        size=state.size,
        game_over=game_over,
        won=won
    )

# ============================================================================
# GUI IMPLEMENTATION
# ============================================================================

class Game2048GUI:
    """GUI implementation for 2048 game"""

    # Color scheme
    COLORS = {
        0: "#CDC1B4",
        2: "#EEE4DA",
        4: "#EDE0C8",
        8: "#F2B179",
        16: "#F59563",
        32: "#F67C5F",
        64: "#F65E3B",
        128: "#EDCF72",
        256: "#EDCC61",
        512: "#EDC850",
        1024: "#EDC53F",
        2048: "#EDC22E",
        "beyond": "#3C3A32"
    }

    TEXT_COLORS = {
        0: "#CDC1B4",
        2: "#776E65",
        4: "#776E65",
        "light": "#F9F6F2",
        "dark": "#776E65"
    }

    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("2048 Game")
        self.root.configure(bg="#FAF8EF")

        # Default game state
        self.state: Optional[GameState] = None
        self.current_size = 4

        # Animation state
        self.animating = False
        self.animation_queue = []

        # Setup GUI
        self.setup_gui()
        self.new_game(4)

        # Bind keyboard events
        self.root.bind("<Key>", self.handle_keypress)

    def setup_gui(self):
        """Setup the GUI components"""
        # Main container
        main_frame = tk.Frame(self.root, bg="#FAF8EF")
        main_frame.pack(padx=20, pady=20)

        # Header
        header_frame = tk.Frame(main_frame, bg="#FAF8EF")
        header_frame.pack(fill=tk.X, pady=(0, 20))

        # Title
        title_label = tk.Label(
            header_frame,
            text="2048",
            font=("Helvetica", 48, "bold"),
            bg="#FAF8EF",
            fg="#776E65"
        )
        title_label.pack(side=tk.LEFT)

        # Score display
        score_frame = tk.Frame(header_frame, bg="#BBADA0", padx=15, pady=5)
        score_frame.pack(side=tk.RIGHT, padx=10)

        tk.Label(
            score_frame,
            text="SCORE",
            font=("Helvetica", 10, "bold"),
            bg="#BBADA0",
            fg="#EEE4DA"
        ).pack()

        self.score_label = tk.Label(
            score_frame,
            text="0",
            font=("Helvetica", 24, "bold"),
            bg="#BBADA0",
            fg="white"
        )
        self.score_label.pack()

        # Controls frame
        controls_frame = tk.Frame(main_frame, bg="#FAF8EF")
        controls_frame.pack(fill=tk.X, pady=(0, 20))

        # New Game button
        new_game_btn = tk.Button(
            controls_frame,
            text="New Game",
            font=("Helvetica", 12, "bold"),
            bg="#8F7A66",
            fg="white",
            padx=15,
            pady=5,
            relief=tk.FLAT,
            cursor="hand2",
            command=lambda: self.new_game(self.current_size)
        )
        new_game_btn.pack(side=tk.LEFT, padx=5)

        # Board size controls
        tk.Label(
            controls_frame,
            text="Board Size:",
            font=("Helvetica", 12),
            bg="#FAF8EF",
            fg="#776E65"
        ).pack(side=tk.LEFT, padx=(20, 5))

        self.size_var = tk.StringVar(value="4")
        size_entry = tk.Entry(
            controls_frame,
            textvariable=self.size_var,
            font=("Helvetica", 12),
            width=5,
            justify=tk.CENTER
        )
        size_entry.pack(side=tk.LEFT, padx=5)

        save_size_btn = tk.Button(
            controls_frame,
            text="Apply",
            font=("Helvetica", 12, "bold"),
            bg="#8F7A66",
            fg="white",
            padx=10,
            pady=5,
            relief=tk.FLAT,
            cursor="hand2",
            command=self.apply_board_size
        )
        save_size_btn.pack(side=tk.LEFT, padx=5)

        # Game board container
        self.board_container = tk.Frame(main_frame, bg="#FAF8EF")
        self.board_container.pack()

        # Instructions
        instructions = tk.Label(
            main_frame,
            text="Use arrow keys or WASD to play",
            font=("Helvetica", 10),
            bg="#FAF8EF",
            fg="#776E65"
        )
        instructions.pack(pady=(10, 0))

    def create_board_grid(self, size: int):
        """Create the game board grid"""
        # Clear existing board
        for widget in self.board_container.winfo_children():
            widget.destroy()

        self.board_frame = tk.Frame(
            self.board_container,
            bg="#BBADA0",
            padx=10,
            pady=10
        )
        self.board_frame.pack()

        # Calculate cell size based on board size
        base_size = 400
        cell_size = base_size // size
        font_size = max(12, 48 - (size - 4) * 6)

        self.cells = []
        for i in range(size):
            row = []
            for j in range(size):
                cell_frame = tk.Frame(
                    self.board_frame,
                    bg="#CDC1B4",
                    width=cell_size,
                    height=cell_size
                )
                cell_frame.grid(row=i, column=j, padx=5, pady=5)
                cell_frame.grid_propagate(False)

                cell_label = tk.Label(
                    cell_frame,
                    text="",
                    font=("Helvetica", font_size, "bold"),
                    bg="#CDC1B4",
                    fg="#CDC1B4"
                )
                cell_label.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

                row.append((cell_frame, cell_label))
            self.cells.append(row)

    def new_game(self, size: int):
        """Start a new game"""
        self.current_size = size
        self.state = initialize_game(size)
        self.create_board_grid(size)
        self.update_display()

    def apply_board_size(self):
        """Apply the board size from entry"""
        try:
            size = int(self.size_var.get())
            if size < 4:
                messagebox.showwarning(
                    "Invalid Size",
                    "Board size must be at least 4x4"
                )
                self.size_var.set(str(self.current_size))
                return
            if size > 10:
                messagebox.showwarning(
                    "Invalid Size",
                    "Board size cannot exceed 10x10 for performance reasons"
                )
                self.size_var.set(str(self.current_size))
                return

            self.new_game(size)

        except ValueError:
            messagebox.showerror(
                "Invalid Input",
                "Please enter a valid number for board size"
            )
            self.size_var.set(str(self.current_size))

    def get_cell_color(self, value: int) -> str:
        """Get background color for a cell value"""
        if value in self.COLORS:
            return self.COLORS[value]
        return self.COLORS["beyond"]

    def get_text_color(self, value: int) -> str:
        """Get text color for a cell value"""
        if value in [0, 2, 4]:
            return self.TEXT_COLORS.get(value, self.TEXT_COLORS["dark"])
        return self.TEXT_COLORS["light"]

    def animate_cell(self, row: int, col: int, value: int, callback=None):
        """Animate a cell with scale effect"""
        if not self.cells or row >= len(self.cells) or col >= len(self.cells[0]):
            if callback:
                callback()
            return

        cell_frame, cell_label = self.cells[row][col]

        # Update value and colors
        display_value = "" if value == 0 else str(value)
        bg_color = self.get_cell_color(value)
        fg_color = self.get_text_color(value)

        cell_label.config(text=display_value, fg=fg_color)
        cell_frame.config(bg=bg_color)
        cell_label.config(bg=bg_color)

        # Scale animation for new tiles
        if value != 0:
            self.scale_animation(cell_frame, callback)
        elif callback:
            callback()

    def scale_animation(self, widget, callback=None, scale=0.8, step=0.1):
        """Create a scale animation effect"""
        if scale < 1.0:
            scale += step
            # Simplified animation - just update quickly
            self.root.after(10, lambda: self.scale_animation(widget, callback, scale, step))
        elif callback:
            callback()

    def update_display(self, animate=False):
        """Update the display with current game state"""
        if not self.state:
            return

        board = self.state.board

        # Update score
        self.score_label.config(text=str(self.state.score))

        # Update cells
        if animate:
            self.animate_board_update(board)
        else:
            for i in range(len(board)):
                for j in range(len(board[0])):
                    value = board[i][j]
                    cell_frame, cell_label = self.cells[i][j]

                    display_value = "" if value == 0 else str(value)
                    bg_color = self.get_cell_color(value)
                    fg_color = self.get_text_color(value)

                    cell_label.config(text=display_value, fg=fg_color)
                    cell_frame.config(bg=bg_color)
                    cell_label.config(bg=bg_color)

        # Check win/lose conditions
        if self.state.won and not hasattr(self, 'won_shown'):
            self.won_shown = True
            self.root.after(300, lambda: messagebox.showinfo(
                "Congratulations!",
                f"You've reached 2048!\nYour score: {self.state.score}\n\nYou can continue playing!"
            ))

        if self.state.game_over:
            self.root.after(300, lambda: self.show_game_over())

    def animate_board_update(self, board):
        """Animate board update"""
        def update_cell(i, j):
            if i < len(board) and j < len(board[0]):
                value = board[i][j]
                self.animate_cell(i, j, value)

        # Update cells with slight delay for effect
        for i in range(len(board)):
            for j in range(len(board[0])):
                self.root.after(i * 10 + j * 5, lambda r=i, c=j: update_cell(r, c))

    def show_game_over(self):
        """Show game over message"""
        result = messagebox.askyesno(
            "Game Over",
            f"No more moves available!\nFinal Score: {self.state.score}\n\nPlay again?"
        )
        if result:
            self.new_game(self.current_size)

    def handle_keypress(self, event):
        """Handle keyboard input"""
        if self.animating or not self.state or self.state.game_over:
            return

        key_map = {
            'Up': Direction.UP,
            'Down': Direction.DOWN,
            'Left': Direction.LEFT,
            'Right': Direction.RIGHT,
            'w': Direction.UP,
            'W': Direction.UP,
            's': Direction.DOWN,
            'S': Direction.DOWN,
            'a': Direction.LEFT,
            'A': Direction.LEFT,
            'd': Direction.RIGHT,
            'D': Direction.RIGHT,
        }

        if event.keysym in key_map:
            self.make_move(key_map[event.keysym])

    def make_move(self, direction: Direction):
        """Make a move in the specified direction"""
        if not self.state or self.animating:
            return

        old_state = self.state
        new_state = apply_move(self.state, direction)

        # Only update if board changed
        if not boards_equal(old_state.board, new_state.board):
            self.animating = True
            self.state = new_state
            self.update_display(animate=True)
            self.root.after(150, lambda: setattr(self, 'animating', False))

def main():
    """Main entry point"""
    root = tk.Tk()
    root.resizable(False, False)
    app = Game2048GUI(root)

    # Center window
    root.update_idletasks()
    width = root.winfo_width()
    height = root.winfo_height()
    x = (root.winfo_screenwidth() // 2) - (width // 2)
    y = (root.winfo_screenheight() // 2) - (height // 2)
    root.geometry(f'{width}x{height}+{x}+{y}')

    root.mainloop()

if __name__ == "__main__":
    main()
