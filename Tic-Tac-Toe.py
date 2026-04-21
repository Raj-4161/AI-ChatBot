"""
Tic-Tac-Toe with Advanced AI and Multiple Game Modes.

This is the main entry point. Run this file to start the game.

Project Structure:
- game.py: Core game logic with Minimax AI
- gui.py: Tkinter GUI interface
- main.py: Main application runner
- Tic-Tac-Toe.py: This file (backwards compatibility)
"""

import tkinter as tk
from gui import TicTacToeGUI

if __name__ == "__main__":
    root = tk.Tk()
    gui = TicTacToeGUI(root)
    root.mainloop()
