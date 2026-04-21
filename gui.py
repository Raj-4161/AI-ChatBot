"""
GUI for Tic-Tac-Toe using Tkinter with difficulty levels.
"""
import tkinter as tk
from tkinter import messagebox
from game import TicTacToeGame


class TicTacToeGUI:
    """
    Tkinter-based GUI for Tic-Tac-Toe game with difficulty selection.
    """
    
    def __init__(self, root):
        self.root = root
        self.root.title("Tic Tac Toe - AI Game")
        self.root.geometry("600x750")
        self.root.configure(bg="#2c3e50")
        
        self.game = TicTacToeGame()
        self.game_active = False
        self.buttons = []
        
        # Color scheme
        self.colors = {
            "bg": "#2c3e50",
            "fg": "#ecf0f1",
            "button_empty": "#34495e",
            "button_x": "#e74c3c",
            "button_o": "#3498db",
            "button_hover": "#7f8c8d"
        }
        
        self.create_widgets()
    
    def create_widgets(self):
        """Create all GUI widgets."""
        # Title
        title = tk.Label(
            self.root,
            text="🎮 Tic Tac Toe",
            font=("Arial", 24, "bold"),
            bg=self.colors["bg"],
            fg=self.colors["fg"]
        )
        title.pack(pady=15)
        
        # Difficulty selection frame
        difficulty_frame = tk.LabelFrame(
            self.root,
            text="Difficulty Level",
            font=("Arial", 12, "bold"),
            bg=self.colors["bg"],
            fg=self.colors["fg"],
            padx=15,
            pady=10
        )
        difficulty_frame.pack(padx=20, pady=10)
        
        self.difficulty_var = tk.StringVar(value="Hard")
        
        for diff in ["Easy", "Medium", "Hard"]:
            rb = tk.Radiobutton(
                difficulty_frame,
                text=diff,
                variable=self.difficulty_var,
                value=diff,
                font=("Arial", 11),
                bg=self.colors["bg"],
                fg=self.colors["fg"],
                selectcolor=self.colors["button_o"],
                command=self.change_difficulty
            )
            rb.pack(side=tk.LEFT, padx=10)
        
        # Status label
        self.status_label = tk.Label(
            self.root,
            text="Select difficulty and click New Game",
            font=("Arial", 12),
            bg=self.colors["bg"],
            fg=self.colors["fg"],
            wraplength=500
        )
        self.status_label.pack(pady=10)
        
        # Game board frame
        board_frame = tk.Frame(self.root, bg=self.colors["bg"])
        board_frame.pack(pady=15)
        
        # Create 3x3 button grid
        for i in range(9):
            btn = tk.Button(
                board_frame,
                text="",
                font=("Arial", 24, "bold"),
                width=6,
                height=3,
                bg=self.colors["button_empty"],
                fg=self.colors["fg"],
                command=lambda pos=i: self.on_button_click(pos),
                relief=tk.RAISED,
                bd=3
            )
            row = i // 3
            col = i % 3
            btn.grid(row=row, column=col, padx=5, pady=5)
            self.buttons.append(btn)
        
        # Control buttons frame
        control_frame = tk.Frame(self.root, bg=self.colors["bg"])
        control_frame.pack(pady=15)
        
        # New Game button
        new_game_btn = tk.Button(
            control_frame,
            text="New Game",
            font=("Arial", 11, "bold"),
            bg="#27ae60",
            fg=self.colors["fg"],
            padx=15,
            pady=8,
            command=self.new_game
        )
        new_game_btn.pack(side=tk.LEFT, padx=5)
        
        # Restart button
        restart_btn = tk.Button(
            control_frame,
            text="Restart",
            font=("Arial", 11, "bold"),
            bg="#e67e22",
            fg=self.colors["fg"],
            padx=15,
            pady=8,
            command=self.restart_game
        )
        restart_btn.pack(side=tk.LEFT, padx=5)
        
        # Stats button
        stats_btn = tk.Button(
            control_frame,
            text="Statistics",
            font=("Arial", 11, "bold"),
            bg="#9b59b6",
            fg=self.colors["fg"],
            padx=15,
            pady=8,
            command=self.show_stats
        )
        stats_btn.pack(side=tk.LEFT, padx=5)
        
        # Stats display frame
        stats_frame = tk.LabelFrame(
            self.root,
            text="📊 Game Statistics",
            font=("Arial", 11, "bold"),
            bg=self.colors["bg"],
            fg=self.colors["fg"],
            padx=15,
            pady=10
        )
        stats_frame.pack(padx=20, pady=10, fill=tk.X)
        
        self.stats_label = tk.Label(
            stats_frame,
            text="Player: 0 | AI: 0 | Draws: 0 | Total: 0",
            font=("Arial", 11),
            bg=self.colors["bg"],
            fg=self.colors["fg"]
        )
        self.stats_label.pack()
    
    def change_difficulty(self):
        """Change AI difficulty level."""
        self.game.difficulty = self.difficulty_var.get()
        if self.game_active:
            self.update_status(f"Difficulty changed to {self.game.difficulty}. Start new game to apply.")
    
    def new_game(self):
        """Start a new game."""
        self.game.reset_board()
        self.game.difficulty = self.difficulty_var.get()
        self.game_active = True
        self.update_board()
        self.update_status("Your turn! Click a cell to move.")
    
    def restart_game(self):
        """Restart current game."""
        if self.game_active:
            self.game.reset_board()
            self.game_active = True
            self.update_board()
            self.update_status("Game restarted! Your turn.")
        else:
            self.new_game()
    
    def on_button_click(self, position):
        """Handle player's button click."""
        if not self.game_active:
            self.update_status("Click 'New Game' to start!")
            return
        
        # Player move
        if not self.game.player_move(position):
            self.update_status("Position already taken!")
            return
        
        self.update_board()
        
        # Check if player won
        if self.game.check_winner("X"):
            self.update_status("🎉 You win!")
            self.game.stats["player_wins"] += 1
            self.game.stats["total_games"] += 1
            self.game_active = False
            self.update_stats()
            return
        
        # Check if draw
        if self.game.is_draw():
            self.update_status("🤝 It's a draw!")
            self.game.stats["draws"] += 1
            self.game.stats["total_games"] += 1
            self.game_active = False
            self.update_stats()
            return
        
        # AI move
        self.root.after(500, self.ai_turn)
    
    def ai_turn(self):
        """Execute AI's turn."""
        if not self.game_active:
            return
        
        move = self.game.get_ai_move()
        
        if move is None:
            self.update_status("🤝 It's a draw!")
            self.game.stats["draws"] += 1
            self.game.stats["total_games"] += 1
            self.game_active = False
            self.update_stats()
            return
        
        self.update_board()
        
        # Check if AI won
        if self.game.check_winner("O"):
            difficulty_text = f"AI wins! ({self.game.difficulty} difficulty)"
            self.update_status(f"🤖 {difficulty_text}")
            self.game.stats["ai_wins"] += 1
            self.game.stats["total_games"] += 1
            self.game_active = False
            self.update_stats()
            return
        
        # Check if draw
        if self.game.is_draw():
            self.update_status("🤝 It's a draw!")
            self.game.stats["draws"] += 1
            self.game.stats["total_games"] += 1
            self.game_active = False
            self.update_stats()
            return
        
        self.update_status("Your turn!")
    
    def update_board(self):
        """Update board display."""
        for i in range(9):
            cell = self.game.board[i]
            if cell == "X":
                self.buttons[i].config(
                    text="X",
                    bg=self.colors["button_x"],
                    state=tk.DISABLED
                )
            elif cell == "O":
                self.buttons[i].config(
                    text="O",
                    bg=self.colors["button_o"],
                    state=tk.DISABLED
                )
            else:
                self.buttons[i].config(
                    text="",
                    bg=self.colors["button_empty"],
                    state=tk.NORMAL
                )
    
    def update_status(self, message):
        """Update status label."""
        self.status_label.config(text=message)
    
    def update_stats(self):
        """Update statistics display."""
        stats = self.game.stats
        stats_text = (
            f"Player: {stats['player_wins']} | "
            f"AI: {stats['ai_wins']} | "
            f"Draws: {stats['draws']} | "
            f"Total: {stats['total_games']}"
        )
        self.stats_label.config(text=stats_text)
    
    def show_stats(self):
        """Show detailed statistics."""
        stats = self.game.stats
        if stats['total_games'] == 0:
            message = "No games played yet!"
        else:
            win_rate = (stats['player_wins'] / stats['total_games']) * 100
            message = (
                f"📊 GAME STATISTICS\n\n"
                f"Player Wins: {stats['player_wins']}\n"
                f"AI Wins: {stats['ai_wins']}\n"
                f"Draws: {stats['draws']}\n"
                f"Total Games: {stats['total_games']}\n"
                f"Win Rate: {win_rate:.1f}%"
            )
        
        messagebox.showinfo("Game Statistics", message)
