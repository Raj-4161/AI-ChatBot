"""
Main entry point for Tic-Tac-Toe game.
Runs the GUI application.
"""
import tkinter as tk
from gui import TicTacToeGUI


if __name__ == "__main__":
    root = tk.Tk()
    gui = TicTacToeGUI(root)
    root.mainloop()
