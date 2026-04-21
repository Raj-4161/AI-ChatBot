"""
Game logic for Tic-Tac-Toe with minimax AI and difficulty levels.
"""
import random


class TicTacToeGame:
    """
    Core game logic for Tic-Tac-Toe with AI and multiple difficulty levels.
    """
    
    def __init__(self):
        """Initialize the game board and statistics."""
        self.board = [" " for _ in range(9)]
        self.memo = {}  # Memoization cache for minimax
        self.stats = {
            "player_wins": 0,
            "ai_wins": 0,
            "draws": 0,
            "total_games": 0
        }
        self.difficulty = "Hard"
        
        # Win conditions
        self.WIN_CONDITIONS = [
            [0,1,2], [3,4,5], [6,7,8],  # Rows
            [0,3,6], [1,4,7], [2,5,8],  # Columns
            [0,4,8], [2,4,6]             # Diagonals
        ]
    
    def get_board_state(self):
        """Convert board to tuple for hashing (memoization)."""
        return tuple(self.board)
    
    def check_winner(self, player):
        """Check if the specified player has won."""
        for condition in self.WIN_CONDITIONS:
            if all(self.board[i] == player for i in condition):
                return True
        return False
    
    def is_draw(self):
        """Check if the board is full (draw condition)."""
        return " " not in self.board
    
    def get_available_moves(self):
        """Return list of available move positions."""
        return [i for i in range(9) if self.board[i] == " "]
    
    def minimax(self, is_maximizing, depth=0):
        """
        Minimax algorithm with memoization.
        Returns the best score for the current board state.
        """
        board_state = self.get_board_state()
        
        # Check memoization cache
        if (board_state, is_maximizing) in self.memo:
            return self.memo[(board_state, is_maximizing)]
        
        # Terminal conditions
        if self.check_winner("O"):  # AI wins
            score = 10 - depth
        elif self.check_winner("X"):  # Player wins
            score = depth - 10
        elif self.is_draw():  # Draw
            score = 0
        else:
            if is_maximizing:  # AI's turn - maximize score
                best_score = -float("inf")
                for i in self.get_available_moves():
                    self.board[i] = "O"
                    score = self.minimax(False, depth + 1)
                    self.board[i] = " "
                    best_score = max(score, best_score)
                score = best_score
            else:  # Player's turn - minimize score
                best_score = float("inf")
                for i in self.get_available_moves():
                    self.board[i] = "X"
                    score = self.minimax(True, depth + 1)
                    self.board[i] = " "
                    best_score = min(score, best_score)
                score = best_score
        
        # Store in memoization cache
        self.memo[(board_state, is_maximizing)] = score
        return score
    
    def ai_move_hard(self):
        """AI move using minimax (Hard difficulty)."""
        best_score = -float("inf")
        move = None
        
        for i in self.get_available_moves():
            self.board[i] = "O"
            score = self.minimax(False)
            self.board[i] = " "
            
            if score > best_score:
                best_score = score
                move = i
        
        if move is not None:
            self.board[move] = "O"
            return move
        return None
    
    def ai_move_medium(self):
        """AI move - medium difficulty (balanced random & strategic)."""
        available = self.get_available_moves()
        
        # 60% strategic, 40% random
        if random.random() < 0.6 and len(available) > 0:
            return self.ai_move_hard()
        else:
            return random.choice(available) if available else None
    
    def ai_move_easy(self):
        """AI move - easy difficulty (random)."""
        available = self.get_available_moves()
        return random.choice(available) if available else None
    
    def get_ai_move(self):
        """Get AI move based on difficulty level."""
        if self.difficulty == "Easy":
            return self.ai_move_easy()
        elif self.difficulty == "Medium":
            return self.ai_move_medium()
        else:  # Hard
            return self.ai_move_hard()
    
    def player_move(self, position):
        """Execute player move at given position (0-8)."""
        if 0 <= position <= 8 and self.board[position] == " ":
            self.board[position] = "X"
            return True
        return False
    
    def reset_board(self):
        """Clear the board for a new game."""
        self.board = [" " for _ in range(9)]
        self.memo = {}
